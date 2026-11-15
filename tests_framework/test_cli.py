import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT/'cli/scrum_sdd.py'


class CLITests(unittest.TestCase):
    def test_version(self):
        r = subprocess.run([sys.executable, CLI, 'version'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), '0.4.6')

    def test_init_preserves_project_data(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t)/'existing'
            (path/'docs').mkdir(parents=True)
            (path/'docs/estado.json').write_text('{"KEEP":true}')
            (path/'CLAUDE.md').write_text('custom instructions')
            (path/'src').mkdir()
            (path/'src/app.py').write_text('existing business code')
            r = subprocess.run([sys.executable, CLI, 'init', str(path)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual((path/'docs/estado.json').read_text(), '{"KEEP":true}')
            self.assertEqual((path/'CLAUDE.md').read_text(), 'custom instructions')
            self.assertEqual((path/'src/app.py').read_text(), 'existing business code')
            self.assertTrue((path/'.framework/scripts/gate.py').is_file())
            self.assertTrue((path/'.claude/skills/ssdd-dercas/SKILL.md').is_file())
            self.assertTrue((path/'.agents/skills/ssdd-dercas/SKILL.md').is_file())
            self.assertTrue((path/'.opencode/commands/ssdd-dercas.md').is_file())
            self.assertTrue((path/'.pi/prompts/ssdd-dercas.md').is_file())
            self.assertTrue((path/'docs/00-fuentes/manuales').is_dir())
            r = subprocess.run([sys.executable, CLI, 'update', str(path)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual((path/'docs/estado.json').read_text(), '{"KEEP":true}')

    def test_agent_selection(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t)/'new'
            r = subprocess.run([sys.executable, CLI, 'init', str(p), '--agent', 'codex'], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((p/'.agents/skills/ssdd-dercas/SKILL.md').is_file())
            self.assertFalse((p/'.claude/skills').exists())

    def test_install_global_without_dependencies(self):
        with tempfile.TemporaryDirectory() as t:
            home = Path(t)
            env = dict(os.environ, HOME=str(home))
            # Forces test out of real user's home by creating temporary isolated HOME.
            r = subprocess.run([sys.executable, ROOT/'install-cli.py'], env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            launcher = home/'.local/bin/ssdd'
            self.assertTrue(launcher.is_file())
            r = subprocess.run([launcher, 'version'], env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.strip(), '0.4.6')


if __name__ == '__main__':
    unittest.main()
