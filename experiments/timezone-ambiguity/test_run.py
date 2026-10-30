import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).with_name('run.py')
spec = importlib.util.spec_from_file_location('timezone_experiment', MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestTimeZoneAmbiguity(unittest.TestCase):
    def test_fold_has_two_real_instants(self):
        x = mod.inspect_local('2026-11-01T01:30:00', 'America/Los_Angeles')
        self.assertEqual(x['status'], 'AMBIGUOUS')
        self.assertEqual([y['utc'] for y in x['valid_utc_candidates']], [
            '2026-11-01T08:30:00Z', '2026-11-01T09:30:00Z'
        ])
        self.assertEqual(x['guard_action'], 'REQUEST_CLARIFICATION')

    def test_skipped_hour_has_no_valid_instant(self):
        x = mod.inspect_local('2026-03-08T02:30:00', 'America/Los_Angeles')
        self.assertEqual(x['status'], 'NONEXISTENT')
        self.assertEqual(x['valid_utc_candidates'], [])
        self.assertEqual(x['guard_action'], 'REQUEST_CLARIFICATION')

    def test_regular_hour_one_instant(self):
        x = mod.inspect_local('2026-10-30T09:00:00', 'America/Los_Angeles')
        self.assertEqual(x['status'], 'UNAMBIGUOUS')
        self.assertEqual(len(x['valid_utc_candidates']), 1)
        self.assertEqual(x['guard_action'], 'ACCEPT')

    def test_after_fall_transition_one_instant(self):
        x = mod.inspect_local('2026-11-01T03:00:00', 'America/Los_Angeles')
        self.assertEqual(x['status'], 'UNAMBIGUOUS')
        self.assertEqual(len(x['valid_utc_candidates']), 1)

    def test_permissive_picks_first_fold(self):
        x = mod.inspect_local('2026-11-01T01:30:00', 'America/Los_Angeles')
        self.assertEqual(x['permissive_fold0_utc'], x['valid_utc_candidates'][0]['utc'])
        self.assertNotEqual(x['valid_utc_candidates'][0]['utc'], x['valid_utc_candidates'][1]['utc'])

    def test_reject_aware_input(self):
        with self.assertRaises(ValueError):
            mod.inspect_local('2026-11-01T01:30:00+00:00', 'America/Los_Angeles')

    def test_evidence_provider_disclosure(self):
        x = mod.evidence()
        self.assertFalse(x['provider_calendar_api_tested'])
        self.assertFalse(x['ai_agent_tested'])
        self.assertEqual(len(x['cases']), 4)


if __name__ == '__main__':
    unittest.main()
