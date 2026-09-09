#!/usr/bin/env python3
"""List provider candidates without making inference or authentication requests."""
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys

HOSTS = {'claude': 'anthropic', 'codex': 'openai', 'gemini': 'google'}
CLIS = [('anthropic', 'claude', 'claude_cli', ['opus', 'sonnet']),
        ('openai', 'codex', 'codex_exec', ['gpt-5.4']),
        ('google', 'gemini', 'gemini_cli', ['gemini-2.5-pro']),
        ('ollama', 'ollama', 'ollama_run', []),
        ('cursor_cli', 'cursor-agent', 'cursor_cli', ['gpt-5.4-high', 'gemini-2.5-pro'])]


def probe(binary, arguments, timeout):
    try:
        with subprocess.Popen([binary, *arguments], stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True, start_new_session=True) as process:
            try:
                output, _ = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
                return 'timeout', ''
            return ('ok' if process.returncode == 0 else 'failed'), output
    except OSError:
        return 'failed', ''


def detect(host, timeout):
    providers = []
    for name, binary, method, defaults in CLIS:
        location = shutil.which(binary)
        native = name == HOSTS[host]
        status, output = ('host', '') if native else ('not_found', '')
        models = list(defaults)
        if location and not native:
            status, output = probe(location, ['list'] if name == 'ollama' else ['--version'], timeout)
        if name == 'ollama' and status == 'ok':
            models = [line.split()[0] for line in output.splitlines()[1:] if line.strip()][:5]
            if not models:
                status = 'no_models'
        providers.append({'name': name, 'available': native or status == 'ok',
                          'installed': native or location is not None,
                          'authenticated': 'unknown', 'inference_ready': 'unknown',
                          'probe_status': status, 'source': 'host' if native else 'cli',
                          'exec_method': 'subagent' if native else method,
                          'binary': 'native' if native else location or 'not_found',
                          'models': ['host-default'] if native and host != 'claude' else models})
    key_present = bool(os.environ.get('NVIDIA_API_KEY'))
    endpoint = 'https://integrate.api.nvidia.com/v1'
    providers.append({'name': 'nvidia_nim', 'available': key_present,
                      'installed': False, 'authenticated': 'unknown', 'inference_ready': 'unknown',
                      'probe_status': 'credential_present' if key_present else 'not_configured',
                      'source': 'environment', 'exec_method': 'openai_compatible_api',
                      'binary': endpoint, 'base_url': endpoint, 'api_key_env': 'NVIDIA_API_KEY',
                      'models': ['deepseek-ai/deepseek-v4-pro', 'deepseek-ai/deepseek-v4-flash']})
    count = sum(p['available'] for p in providers)
    return {'schema_version': 2, 'host': host, 'host_provider': HOSTS[host],
            'providers': providers, 'provider_count': count, 'multi_provider': count >= 2,
            'availability_semantics': 'dispatch candidates only; auth and inference unverified'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=list(HOSTS), default='claude')
    args = parser.parse_args()
    try:
        timeout = float(os.environ.get('COUNCIL_DETECT_TIMEOUT', '5'))
        if not 0 < timeout <= 30:
            raise ValueError('COUNCIL_DETECT_TIMEOUT must be in (0, 30]')
        print(json.dumps(detect(args.host, timeout)))
    except ValueError as exc:
        print(json.dumps({'error': str(exc)}))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
