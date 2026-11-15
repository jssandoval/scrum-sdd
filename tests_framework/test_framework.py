import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.p = pathlib.Path(self.temp.name)
        install = run(['bash', str(ROOT / 'install.sh'), str(self.p)], self.p)
        self.assertEqual(install.returncode, 0, install.stderr)

    def gate(self, *args):
        return run([sys.executable, '.framework/scripts/gate.py', *args], self.p)

    def trace(self, *args):
        return run([sys.executable, '.framework/scripts/trace.py', *args], self.p)

    def fixture(self):
        (self.p/'docs/02-requisitos/DERCAS.md').write_text('''# DERCAS
### RF-001 Registro
**Prioridad:** Must
### CA-001 (RF-001) Guarda cliente
Dado el cliente
Cuando se registra
Entonces se guarda
''')
        (self.p/'docs/05-scrum/product-backlog.md').write_text('''# Backlog
### HU-001 Registrar cliente
**Requisitos:** RF-001
**Criterios:** CA-001
''')
        (self.p/'specs/HU-001.md').write_text('# HU-001\nEspecificación completa\n')

    def test_instalacion(self):
        self.assertTrue((self.p/'.claude/skills/aceptar/SKILL.md').exists())
        self.assertTrue((self.p/'.framework/scripts/gate.py').exists())

    def test_no_acepta_historia_sin_evidencia(self):
        self.assertNotEqual(self.gate('hu','HU-001','especificada').returncode, 0)
        self.fixture()
        self.assertEqual(self.gate('hu','HU-001','especificada').returncode, 0)
        self.assertNotEqual(self.gate('hu','HU-001','implementada').returncode, 0)

    def test_trace_no_cuenta_assert_true(self):
        self.fixture()
        tests = self.p/'tests'
        tests.mkdir(exist_ok=True)
        (tests/'test_cliente.py').write_text('def test_cliente():\n    # CA-001\n    assert True\n')
        self.assertNotEqual(self.trace('--hu','HU-001').returncode, 0)
        (tests/'test_cliente.py').write_text('def test_cliente():\n    # CA-001\n    assert sumar_cliente() == 1\n')
        self.assertEqual(self.trace('--hu','HU-001').returncode, 0)

    def test_transiciones_requieren_informe(self):
        self.fixture()
        tests = self.p/'tests'
        tests.mkdir(exist_ok=True)
        (tests/'test_cliente.py').write_text('def test_cliente():\n    # CA-001\n    assert sumar_cliente() == 1\n')
        self.assertEqual(self.gate('hu','HU-001','especificada').returncode,0)
        self.assertEqual(self.gate('hu','HU-001','implementada').returncode,0)
        self.assertNotEqual(self.gate('hu','HU-001','auditada').returncode,0)
        report=self.p/'docs/06-pruebas/auditoria-HU-001.md'
        report.write_text('# Auditoría HU-001\nVeredicto: Aprobado\n')
        self.assertEqual(self.gate('hu','HU-001','auditada').returncode,0)
        self.assertNotEqual(self.gate('hu','HU-001','aceptada').returncode,0)
        self.assertEqual(self.gate('hu','HU-001','aceptada','--por','Humano').returncode,0)
        self.assertNotEqual(self.gate('hu','HU-001','implementada').returncode,0)

    def test_aprobacion_invalida_al_editar(self):
        doc = self.p/'docs/01-descubrimiento/vision-producto.md'
        doc.write_text('versión original')
        self.assertEqual(self.gate('approve','descubrimiento','--por','Humano').returncode,0)
        doc.write_text('modificado')
        self.assertNotEqual(self.gate('check','requisitos').returncode,0)

    def test_instala_carpetas_de_fuentes_y_plantillas(self):
        self.assertTrue((self.p/'docs/00-fuentes/manuales').is_dir())
        self.assertTrue((self.p/'docs/00-fuentes/matrices').is_dir())
        self.assertTrue((self.p/'.framework/scripts/fuentes.py').exists())
        self.assertTrue((self.p/'.framework/templates/analisis-fuentes.md').exists())

    def test_inventario_detecta_cambio_de_contenido(self):
        folder = self.p/'docs/00-fuentes/manuales'
        f = folder/'operacion.md'
        f.write_text('# Manual\nCampo obligatorio')
        script = [sys.executable, '.framework/scripts/fuentes.py']
        self.assertEqual(run(script+['scan'], self.p).returncode, 0)
        self.assertEqual(run(script+['check'], self.p).returncode, 0)
        f.write_text('# Manual\nCampo opcional')
        self.assertNotEqual(run(script+['check'], self.p).returncode, 0)
        self.assertEqual(run(script+['scan'], self.p).returncode, 0)
        self.assertEqual(run(script+['check'], self.p).returncode, 0)

    def test_cambio_de_fuente_invalida_aprobaciones(self):
        fuente = self.p/'docs/00-fuentes/manuales/manual.md'
        fuente.write_text('Versión uno')
        for d in ('docs/01-descubrimiento/vision-producto.md', 'docs/02-requisitos/DERCAS.md'):
            (self.p/d).write_text('Documento revisado')
        self.assertEqual(self.gate('approve','descubrimiento','--por','Humano').returncode, 0)
        self.assertEqual(self.gate('approve','requisitos','--por','Humano').returncode, 0)
        fuente.write_text('Versión dos')
        self.assertNotEqual(self.gate('check','requisitos').returncode, 0)
        self.assertNotEqual(self.gate('check','diseno').returncode, 0)

    def test_ejemplo_dos_fuentes_con_conflicto(self):
        example = ROOT/'examples/registro-clientes/fuentes'
        self.assertTrue((example/'manuales/manual-registro.md').exists())
        self.assertTrue((example/'formularios/formulario-alta.md').exists())
        manual=(example/'manuales/manual-registro.md').read_text()
        form=(example/'formularios/formulario-alta.md').read_text()
        self.assertIn('teléfono de contacto es obligatorio', manual)
        self.assertIn('Teléfono: opcional', form)


if __name__ == '__main__':
    unittest.main()
