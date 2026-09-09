import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def test_each_client_installs_a_self_contained_protocol_and_runtime(self):
        cases = [([], '--claude-dir', 'skills/council'),
                 (['--codex-only'], '--codex-dir', 'skills/council'),
                 (['--gemini-only'], '--gemini-dir',
                  'extensions/council-of-high-intelligence/skills/council')]
        for flags, target_flag, suffix in cases:
            with self.subTest(client=target_flag), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / 'client with spaces'
                result = subprocess.run(['/bin/bash', str(ROOT / 'install.sh'),
                                         *flags, target_flag, str(target)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                skill = target / suffix
                for relative in ['protocol/core.md', 'protocol/runtime.md',
                                 'scripts/council_runtime.py', 'scripts/detect_providers.py',
                                 'configs/auto-route-defaults.yaml']:
                    self.assertTrue((skill / relative).is_file(), f'Missing installed {relative}')
                result = subprocess.run([sys.executable, str(skill / 'scripts/council_runtime.py'),
                                         'route'], input=json.dumps({'members': [{'id': 'ada'}],
                                                                    'providers': []}),
                                        capture_output=True, text=True, cwd=directory)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'], 'analysis_only')

    def test_dry_run_does_not_create_target(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'untouched'
            result = subprocess.run(['/bin/bash', str(ROOT / 'install.sh'), '--codex-only',
                                     '--codex-dir', str(target), '--dry-run'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(target.exists())


if __name__ == '__main__':
    unittest.main()
