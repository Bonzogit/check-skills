#!/usr/bin/env python3
"""Check declared coverage, current evidence and recheck links; never certify quality."""
import argparse,json
from datetime import datetime
from pathlib import Path

def text(value):return isinstance(value,str) and bool(value.strip())
def local_file(root,value):
 if not text(value) or '\\' in value or ':' in value:return False
 try:
  p=Path(value)
  if p.is_absolute() or '..' in p.parts:return False
  target=(root/p).resolve()
  return target.is_relative_to(root) and target.is_file() and target.stat().st_size>0
 except (OSError,ValueError,TypeError):return False
def validate(root,report,version,require_pass=False):
 root=Path(root).resolve();errors=[];unresolved=[];missing=[];coverage={};check_map={}
 def need(ok,message):
  if not ok:errors.append(message)
 def rows(value,where):
  if not isinstance(value,list):errors.append(where+': expected array');return []
  result=[]
  for row in value:
   if not isinstance(row,dict):errors.append(where+': expected object');continue
   result.append(row)
  return result
 def evidence(value,where,required=False):
  if not isinstance(value,list):errors.append(where+': evidence must be array');return
  if required:need(bool(value),where+': evidence required')
  for path in value:need(local_file(root,path),where+': missing, empty or unsafe evidence: '+str(path))
 if not isinstance(report,dict):return {'recordStructurePassed':False,'declaredChecksPassed':False,'websiteQualityCertified':False,'errors':['Report must be object'],'unresolvedFindings':[],'coverageRecorded':False,'missingChecks':[]}
 schema=report.get('schemaVersion');modern=schema=='1.1'
 need(schema in ('1.0','1.1'),'Unsupported schemaVersion');need(text(version) and report.get('projectVersion')==version,'Report version differs from target')
 scope=report.get('scope',{})
 need(isinstance(scope,dict) and scope.get('mode') in ('sample','full','change','deployment') and isinstance(scope.get('affected'),list) and bool(scope['affected']) and all(text(x) for x in scope['affected']),'Scope needs mode and affected areas')
 need(text(report.get('executor')),'Actual executor is required')
 if modern:
  planned=rows(report.get('coverage'),'coverage');need(bool(planned),'No planned coverage recorded')
  for row in planned:
   ident=row.get('id');valid=text(ident)
   need(valid and ident not in coverage,'Missing or duplicate coverage ID')
   if valid:coverage[ident]=row
   for key in ('basis','expected','page','environment'):need(text(row.get(key)),str(ident)+': coverage missing '+key)
 checks=rows(report.get('checks',[]),'checks');need(bool(checks),'No checks recorded')
 for row in checks:
  ident=row.get('id');valid=text(ident)
  need(valid and ident not in check_map,'Missing or duplicate check ID')
  if valid:check_map[ident]=row
  status=row.get('status');need(status in ('pass','fail','unverified','not-applicable'),str(ident)+': invalid status');need(text(row.get('result')),str(ident)+': observable result or limitation required')
  if modern:need(valid and ident in coverage,str(ident)+': check is not in declared coverage')
  if status=='not-applicable':need(text(row.get('reason')),str(ident)+': not-applicable reason required')
  evidence(row.get('evidence',[]),str(ident),required=status=='pass')
  if status=='pass':
   for key in ('method','page','viewport','observedAt'):need(text(row.get(key)),str(ident)+': missing '+key)
   need(row.get('version')==version,str(ident)+': stale evidence version')
   try:
    date=datetime.fromisoformat(row.get('observedAt','').replace('Z','+00:00'));need(date.tzinfo is not None,str(ident)+': timestamp must specify timezone')
   except (ValueError,TypeError,AttributeError):errors.append(str(ident)+': invalid timestamp')
   if modern and valid and ident in coverage:
    need(row.get('page')==coverage[ident].get('page'),str(ident)+': evidence page differs from planned page')
    need(text(row.get('environment')) and row.get('environment')==coverage[ident].get('environment'),str(ident)+': evidence environment differs from plan')
 if modern:
  missing=sorted(set(coverage)-set(check_map))
  for ident in missing:errors.append(ident+': planned check missing; record unverified instead of omitting')
 findings=rows(report.get('findings',[]),'findings');finding_ids=set()
 for row in findings:
  ident=row.get('id');valid=text(ident);need(valid and ident not in finding_ids,'Missing or duplicate finding ID')
  if valid:finding_ids.add(ident)
  state=row.get('state');need(state in ('open','fixed-awaiting-recheck','verified','accepted'),'Invalid finding state')
  for key in ('ownerStage','expected','actual','reproduce'):need(text(row.get(key)),'Finding missing '+key)
  if modern:
   need(row.get('severity') in ('blocker','major','minor','suggestion'),'Finding needs severity');need(text(row.get('impact')),'Finding needs user impact')
   affected=row.get('affectedChecks');good=isinstance(affected,list) and bool(affected) and all(text(x) and x in coverage for x in affected)
   need(good,'Finding needs affectedChecks from declared coverage')
  if state!='verified':unresolved.append(ident)
  else:
   recheck=row.get('verifiedByCheck');passed=text(recheck) and recheck in check_map and check_map[recheck].get('status')=='pass'
   need(passed,'Verified finding lacks passing recheck')
   if modern:
    need(good and recheck in affected,'Verified finding uses unrelated recheck')
    if good:need(all(check_map.get(x,{}).get('status')=='pass' for x in affected),'Verified finding has affected checks still incomplete')
 declared=bool(checks) and all(c.get('status') in ('pass','not-applicable') for c in checks) and not unresolved and not errors
 if require_pass and not declared:errors.append('Applicable checks incomplete or findings unresolved')
 return {'recordStructurePassed':not errors,'declaredChecksPassed':declared,'websiteQualityCertified':False,'errors':errors,'unresolvedFindings':unresolved,'coverageRecorded':modern and bool(coverage),'missingChecks':missing}

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('project');parser.add_argument('--report',default='docs/review-report.json');parser.add_argument('--version',required=True);parser.add_argument('--require-pass',action='store_true');args=parser.parse_args();root=Path(args.project).resolve()
 if not local_file(root,args.report):parser.exit(2,'Report must be a nonempty local file with a safe relative path\n')
 try:report=json.loads((root/args.report).read_text('utf-8-sig'));result=validate(root,report,args.version,args.require_pass)
 except (OSError,ValueError,TypeError) as error:parser.exit(2,str(error)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['recordStructurePassed'] else 1)
if __name__=='__main__':main()
