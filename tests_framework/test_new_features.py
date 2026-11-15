import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT/'cli/scrum_sdd.py'

class FeatureTests(unittest.TestCase):
    def run_cmd(self, cwd, *args):
        return subprocess.run([sys.executable, *map(str,args)], cwd=cwd, text=True, capture_output=True)

    def test_architecture_requires_human_stack_selection(self):
        p = (ROOT/'skills/ssdd-arquitectura/SKILL.md').read_text(encoding='utf-8')
        for field in ('frontend','backend','interoperabilidad','persistencia','infraestructura'):
            self.assertIn(field, p.lower())
        self.assertIn('DETENERSE', p)

    def test_revert_archives_and_invalidates_downstream(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            a = d/'docs/04-arquitectura'
            a.mkdir(parents=True)
            (a/'arquitectura-c4.md').write_text('diagrama original',encoding='utf-8')
            state = {'fases': {
                'descubrimiento': {'por':'Persona','fecha':'2026-01-01','sha256':'abc'},
                'arquitectura': {'por':'Persona','fecha':'2026-01-02','sha256':'def'},
                'backlog': {'por':'Persona','fecha':'2026-01-03','sha256':'xyz'},
            },'hu':{'HU-001':{'estado':'implementada'}}}
            (d/'docs/estado.json').write_text(json.dumps(state),encoding='utf-8')
            q=self.run_cmd(d,ROOT/'scripts/gate.py','revert','arquitectura','--por','Persona','--motivo','Cambiar stack')
            self.assertEqual(q.returncode,0,q.stdout+q.stderr)
            now=json.loads((d/'docs/estado.json').read_text())
            self.assertIn('descubrimiento',now['fases'])
            self.assertNotIn('arquitectura',now['fases'])
            self.assertNotIn('backlog',now['fases'])
            self.assertIn('HU-001',now['hu'])
            archive=list((d/'docs/historico-fases').iterdir())
            self.assertEqual(len(archive),1)
            self.assertTrue((archive[0]/'estado-anterior.json').exists())
            self.assertTrue((archive[0]/'reversion.json').exists())
            self.assertEqual((archive[0]/'docs/04-arquitectura/arquitectura-c4.md').read_text(),'diagrama original')
            self.assertTrue((a/'arquitectura-c4.md').exists())
            bad=self.run_cmd(d,ROOT/'scripts/gate.py','revert','arquitectura','--por','Persona','--motivo','repetir')
            self.assertNotEqual(bad.returncode,0)

    def test_update_existing_project_installs_new_skill_preserves_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            s=d/'docs';s.mkdir()
            (s/'estado.json').write_text('{"fases":{},"hu":{}}')
            (s/'02-requisitos').mkdir()
            (s/'02-requisitos/DERCAS.md').write_text('MIS REQUISITOS')
            (d/'src').mkdir();(d/'src/example.py').write_text('keep')
            z=self.run_cmd(d,CLI,'update',str(d))
            self.assertEqual(z.returncode,0,z.stderr)
            self.assertTrue((d/'.agents/skills/ssdd-revertir/SKILL.md').exists())
            self.assertTrue((d/'.claude/skills/ssdd-revertir/SKILL.md').exists())
            self.assertTrue((d/'.opencode/commands/ssdd-revertir.md').exists())
            self.assertEqual((s/'02-requisitos/DERCAS.md').read_text(),'MIS REQUISITOS')
            self.assertEqual((d/'src/example.py').read_text(),'keep')
            self.assertEqual((d/'.framework/VERSION').read_text().strip(),'0.4.6')

if __name__=='__main__': unittest.main()
