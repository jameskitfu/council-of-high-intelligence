"""Only external version probes are faked; the detector itself runs."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DetectionTests(unittest.TestCase):
    def detect(self, host, fake=None):
        with tempfile.TemporaryDirectory(prefix='council-"quoted-') as directory:
            if fake:
                path = Path(directory) / 'codex'
                path.write_text('#!/bin/sh\n' + fake)
                path.chmod(0o755)
            env = {**os.environ, 'PATH': directory + ':/usr/bin:/bin',
                   'COUNCIL_DETECT_TIMEOUT': '0.1'}
            env.pop('NVIDIA_API_KEY', None)
            result = subprocess.run(['/bin/bash', str(ROOT / 'scripts/detect-providers.sh'),
                                     '--host', host], env=env, capture_output=True,
                                    text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError as exc:
                self.fail(f'Detector emitted invalid JSON for a quoted CLI path: {exc}')
            self.assertIn('host', data, 'Detector must identify its actual host')
            self.assertEqual(data['host'], host)
            return data

    def test_codex_host_does_not_invent_anthropic_runtime(self):
        data = self.detect('codex')
        available = {p['name'] for p in data['providers'] if p['available']}
        self.assertEqual(available, {'openai'})
        native = next(p for p in data['providers'] if p['name'] == 'openai')
        self.assertEqual(native['exec_method'], 'subagent')

    def test_gemini_host_is_google(self):
        data = self.detect('gemini')
        self.assertEqual({p['name'] for p in data['providers'] if p['available']}, {'google'})

    def test_installed_cli_does_not_claim_authentication_or_inference(self):
        data = self.detect('claude', 'echo codex-test-version\n')
        cli = next(p for p in data['providers'] if p['name'] == 'openai')
        self.assertTrue(cli['installed'])
        self.assertEqual(cli['authenticated'], 'unknown')
        self.assertEqual(cli['inference_ready'], 'unknown')
        self.assertIn('"quoted-', cli['binary'])

    def test_hung_cli_probe_is_bounded(self):
        data = self.detect('claude', 'sleep 30\n')
        cli = next(p for p in data['providers'] if p['name'] == 'openai')
        self.assertTrue(cli['installed'])
        self.assertFalse(cli['available'])
        self.assertEqual(cli['probe_status'], 'timeout')


if __name__ == '__main__':
    unittest.main()
