import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('node'), 'node is required for the MiMo Code plugin')
class MiMoCodePluginTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.env = os.environ.copy()
        self.env['XDG_CONFIG_HOME'] = str(self.root / 'config')
        self.env.pop('MIMOCODE_HOME', None)

    def run_plugin(self, mode, config=None):
        args = ['node', str(ROOT / 'tests/opencode_plugin_driver.mjs'),
                str(ROOT / '.mimocode/plugins/i-have-adhd.mjs'), mode]
        if config is not None:
            args.append(json.dumps(config))
        return subprocess.run(args, env=self.env, text=True, capture_output=True, check=True).stdout

    def test_explicit_command_delivers_ruleset_without_model_skill_invocation(self):
        config = json.loads(self.run_plugin('v1-config'))
        template = config['command']['i-have-adhd']['template']
        self.assertIn('Working memory is small', template)
        self.assertIn('stop adhd mode', template)
        self.assertNotIn('disable-model-invocation:', template)
        self.assertEqual([str(ROOT / 'skills')], config['skills']['paths'])

    def test_preserves_other_configuration_and_user_command(self):
        existing = {'command': {'i-have-adhd': {'template': 'user command'}, 'other': {'template': 'keep'}},
                    'skills': {'paths': ['/other/skills']}}
        config = json.loads(self.run_plugin('v1-config', existing))
        self.assertEqual(existing['command'], config['command'])
        self.assertEqual(['/other/skills', str(ROOT / 'skills')], config['skills']['paths'])

    def test_always_on_requires_mimocode_flag(self):
        self.assertEqual('', self.run_plugin('v1-context'))
        wrong = self.root / 'config/opencode/.i-have-adhd-always'
        wrong.parent.mkdir(parents=True)
        wrong.touch()
        self.assertEqual('', self.run_plugin('v1-context'))
        flag = self.root / 'config/mimocode/.i-have-adhd-always'
        flag.parent.mkdir(parents=True)
        flag.touch()
        self.assertIn('Working memory is small', self.run_plugin('v1-context'))
        flag.unlink()
        self.assertEqual('', self.run_plugin('v1-context'))

    def test_mimocode_home_overrides_xdg_for_opt_in(self):
        self.env['MIMOCODE_HOME'] = str(self.root / 'mimo-home')
        flag = self.root / 'mimo-home/config/.i-have-adhd-always'
        flag.parent.mkdir(parents=True)
        flag.touch()
        self.assertIn('Working memory is small', self.run_plugin('v1-context'))
