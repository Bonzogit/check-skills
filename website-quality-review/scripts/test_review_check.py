import copy
import tempfile
import unittest
from pathlib import Path
from review_check import validate


class ReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'evidence.txt').write_text('Synthetic evidence fixture; no browser was run.', encoding='utf-8')
        self.report = {'schemaVersion': '1.0', 'projectVersion': '1', 'scope': {'mode': 'sample', 'affected': ['form']}, 'executor': 'fixture', 'checks': [{'id': 'form', 'status': 'pass', 'method': 'synthetic test', 'page': '/contact', 'viewport': 'not applicable: record test', 'observedAt': '2026-10-16T00:00:00Z', 'version': '1', 'evidence': ['evidence.txt'], 'result': 'Fixture only'}], 'findings': []}

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_record_does_not_certify_website(self):
        result = validate(self.root, self.report, '1', True)
        self.assertTrue(result['recordStructurePassed'])
        self.assertFalse(result['websiteQualityCertified'])

    def test_stale_version_rejected(self):
        self.report['checks'][0]['version'] = 'old'
        self.assertFalse(validate(self.root, self.report, '1')['recordStructurePassed'])

    def test_outside_and_empty_evidence_rejected(self):
        for path in ('../outside.txt', 'missing.txt'):
            self.report['checks'][0]['evidence'] = [path]
            self.assertFalse(validate(self.root, self.report, '1')['recordStructurePassed'])
        (self.root / 'evidence.txt').write_text('')
        self.report['checks'][0]['evidence'] = ['evidence.txt']
        self.assertFalse(validate(self.root, self.report, '1')['recordStructurePassed'])

    def test_unverified_is_honest_but_not_complete(self):
        self.report['checks'][0]['status'] = 'unverified'
        self.assertTrue(validate(self.root, self.report, '1')['recordStructurePassed'])
        self.assertFalse(validate(self.root, self.report, '1', True)['recordStructurePassed'])

    def test_unresolved_or_false_recheck_rejected(self):
        finding = {'id': 'f1', 'ownerStage': 'build', 'expected': 'saved', 'actual': 'failed', 'reproduce': 'submit', 'state': 'open'}
        self.report['findings'] = [finding]
        self.assertFalse(validate(self.root, self.report, '1', True)['recordStructurePassed'])
        finding.update(state='verified', verifiedByCheck='missing')
        self.assertFalse(validate(self.root, self.report, '1')['recordStructurePassed'])
        finding['verifiedByCheck'] = 'form'
        self.assertTrue(validate(self.root, self.report, '1', True)['recordStructurePassed'])

    def test_not_applicable_requires_reason(self):
        self.report['checks'][0]['status'] = 'not-applicable'
        self.assertFalse(validate(self.root, self.report, '1')['recordStructurePassed'])


if __name__ == '__main__':
    unittest.main()
