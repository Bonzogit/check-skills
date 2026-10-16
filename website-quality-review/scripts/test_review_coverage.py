import copy,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from review_check import validate

class Coverage(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);(self.root/'proof.txt').write_text('Synthetic record fixture, no browser executed.',encoding='utf-8')
  self.report={'schemaVersion':'1.1','projectVersion':'site-2','scope':{'mode':'change','affected':['menu']},'executor':'fixture','coverage':[{'id':'menu','basis':'Current request','expected':'Return preserves reading position','page':'/','environment':'desktop-chromium'}],'checks':[{'id':'menu','status':'pass','result':'Synthetic fixture','version':'site-2','method':'record fixture','page':'/','viewport':'1440x900','environment':'desktop-chromium','observedAt':'2026-10-16T12:00:00+08:00','evidence':['proof.txt']}],'findings':[]}
 def result(self,strict=False):return validate(self.root,self.report,'site-2',strict)
 def finding(self):return {'id':'f1','ownerStage':'build','expected':'Reading position retained','actual':'Position lost','reproduce':'Close menu','severity':'major','impact':'Visitor loses place','affectedChecks':['menu'],'state':'verified','verifiedByCheck':'menu'}
 def test_valid_coverage_never_certifies_website(self):
  r=self.result(True);self.assertTrue(r['recordStructurePassed'],r);self.assertTrue(r['coverageRecorded']);self.assertTrue(r['declaredChecksPassed']);self.assertFalse(r['websiteQualityCertified'])
 def test_omitted_planned_check_rejected(self):
  self.report['coverage'].append({**self.report['coverage'][0],'id':'mobile','environment':'mobile-webkit'});r=self.result();self.assertFalse(r['declaredChecksPassed']);self.assertEqual(r['missingChecks'],['mobile'])
 def test_unverified_is_recorded_without_claiming_completion(self):
  self.report['checks'][0]['status']='unverified';r=self.result();self.assertTrue(r['recordStructurePassed']);self.assertFalse(r['declaredChecksPassed'])
 def test_wrong_page_or_environment_rejected(self):
  for key,value in [('page','/other'),('environment','mobile-webkit')]:
   before=self.report['checks'][0][key];self.report['checks'][0][key]=value;self.assertFalse(self.result()['recordStructurePassed']);self.report['checks'][0][key]=before
 def test_unplanned_passing_check_rejected(self):
  self.report['checks'].append({**self.report['checks'][0],'id':'other'});self.assertFalse(self.result()['recordStructurePassed'])
 def test_unrelated_recheck_cannot_close_finding(self):
  self.report['coverage'].append({**self.report['coverage'][0],'id':'other'});self.report['checks'].append({**self.report['checks'][0],'id':'other'});f=self.finding();f['verifiedByCheck']='other';self.report['findings']=[f];self.assertFalse(self.result()['recordStructurePassed'])
 def test_all_affected_checks_must_be_rechecked(self):
  self.report['coverage'].append({**self.report['coverage'][0],'id':'mobile'});self.report['checks'].append({**self.report['checks'][0],'id':'mobile','status':'unverified'});f=self.finding();f['affectedChecks'].append('mobile');self.report['findings']=[f];self.assertFalse(self.result()['recordStructurePassed'])
 def test_related_recheck_can_close_finding(self):
  self.report['findings']=[self.finding()];self.assertTrue(self.result(True)['declaredChecksPassed'])
 def test_duplicate_finding_rejected(self):
  self.report['findings']=[self.finding(),self.finding()];self.assertFalse(self.result()['recordStructurePassed'])
 def test_malformed_input_returns_fail_instead_of_crashing(self):
  for value in [None,[],{'schemaVersion':'1.1','scope':[],'checks':[None],'coverage':[None],'findings':[None]}]:self.assertFalse(validate(self.root,value,'site-2')['recordStructurePassed'])
 def test_portable_paths_and_bad_timestamp_rejected(self):
  for value in ['..'+chr(92)+'proof.txt','sub/../proof.txt','Z:proof.txt','proof.txt'+chr(0)]:
   self.report['checks'][0]['evidence']=[value];self.assertFalse(self.result()['recordStructurePassed'])
  self.report['checks'][0]['evidence']=['proof.txt'];self.report['checks'][0]['observedAt']=None;self.assertFalse(self.result()['recordStructurePassed'])
 def test_errors_cannot_report_declared_pass_even_for_legacy(self):
  self.report['schemaVersion']='1.0';self.report['checks'][0]['version']='stale';r=self.result();self.assertFalse(r['declaredChecksPassed']);self.assertFalse(r['coverageRecorded'])
 def test_relocated_checker_runs_from_another_working_directory(self):
  moved=self.root/'new-device';moved.mkdir();shutil.copyfile(Path(__file__).with_name('review_check.py'),moved/'review_check.py')
  (self.root/'docs').mkdir();(self.root/'docs/review-report.json').write_text(json.dumps(self.report),encoding='utf-8')
  r=subprocess.run([sys.executable,str(moved/'review_check.py'),str(self.root),'--version','site-2','--require-pass'],cwd=moved,capture_output=True,text=True,encoding='utf-8');self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(json.loads(r.stdout)['declaredChecksPassed'])

if __name__=='__main__':unittest.main()
