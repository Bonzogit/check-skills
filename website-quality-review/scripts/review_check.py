#!/usr/bin/env python3
"""Validate review records and evidence paths; never certify rendered website quality."""
import argparse
import json
from datetime import datetime
from pathlib import Path


def validate(root, report, version, require_pass=False):
    root = Path(root).resolve()
    errors = []
    if report.get('schemaVersion') != '1.0':
        errors.append('Unsupported schemaVersion')
    if report.get('projectVersion') != version:
        errors.append('Report version differs from target')
    scope = report.get('scope', {})
    if scope.get('mode') not in ('sample', 'full', 'change', 'deployment') or not scope.get('affected'):
        errors.append('Scope needs mode and affected areas')
    if not report.get('executor'):
        errors.append('Actual executor is required')
    checks = report.get('checks', [])
    if not isinstance(checks, list) or not checks:
        errors.append('No checks recorded')
        checks = []
    ids = set()
    for row in checks:
        identity = row.get('id')
        if not identity or identity in ids:
            errors.append('Missing or duplicate check ID')
        ids.add(identity)
        status = row.get('status')
        if status not in ('pass', 'fail', 'unverified', 'not-applicable'):
            errors.append(f'{identity}: invalid status')
        if not row.get('result'):
            errors.append(f'{identity}: observable result or limitation required')
        if status == 'not-applicable' and not row.get('reason'):
            errors.append(f'{identity}: not-applicable reason required')
        if status == 'pass':
            for key in ('method', 'page', 'viewport', 'observedAt'):
                if not row.get(key):
                    errors.append(f'{identity}: missing {key}')
            if row.get('version') != version:
                errors.append(f'{identity}: stale evidence version')
            try:
                date = datetime.fromisoformat(row.get('observedAt', '').replace('Z', '+00:00'))
                if date.tzinfo is None:
                    errors.append(f'{identity}: timestamp must specify timezone')
            except ValueError:
                errors.append(f'{identity}: invalid timestamp')
            if not row.get('evidence'):
                errors.append(f'{identity}: evidence required')
            for relative in row.get('evidence', []):
                if not isinstance(relative, str):
                    errors.append(f'{identity}: evidence path must be text')
                    continue
                path = (root / relative).resolve()
                if Path(relative).is_absolute() or not path.is_relative_to(root):
                    errors.append(f'{identity}: evidence leaves project')
                elif not path.is_file() or path.stat().st_size == 0:
                    errors.append(f'{identity}: missing or empty evidence')
    findings = report.get('findings', [])
    unresolved = []
    for row in findings:
        if row.get('state') not in ('open', 'fixed-awaiting-recheck', 'verified', 'accepted'):
            errors.append('Invalid finding state')
        for key in ('id', 'ownerStage', 'expected', 'actual', 'reproduce'):
            if not row.get(key):
                errors.append(f'Finding missing {key}')
        if row.get('state') != 'verified':
            unresolved.append(row.get('id'))
        elif row.get('verifiedByCheck') not in ids or not any(c.get('id') == row.get('verifiedByCheck') and c.get('status') == 'pass' for c in checks):
            errors.append('Verified finding lacks passing recheck')
    declared_pass = bool(checks) and all(c.get('status') in ('pass', 'not-applicable') for c in checks) and not unresolved
    if require_pass and not declared_pass:
        errors.append('Applicable checks incomplete or findings unresolved')
    return {'recordStructurePassed': not errors, 'declaredChecksPassed': declared_pass,
            'websiteQualityCertified': False, 'errors': errors, 'unresolvedFindings': unresolved}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project')
    parser.add_argument('--report', default='docs/review-report.json')
    parser.add_argument('--version', required=True)
    parser.add_argument('--require-pass', action='store_true')
    args = parser.parse_args()
    root = Path(args.project).resolve()
    report_path = (root / args.report).resolve()
    if not report_path.is_relative_to(root):
        parser.exit(2, 'Report must stay in project\n')
    try:
        report = json.loads(report_path.read_text(encoding='utf-8-sig'))
        result = validate(root, report, args.version, args.require_pass)
    except (OSError, ValueError, TypeError) as error:
        parser.exit(2, str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['recordStructurePassed'] else 1)


if __name__ == '__main__':
    main()
