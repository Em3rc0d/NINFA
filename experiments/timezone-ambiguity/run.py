#!/usr/bin/env python3
"""NINFA S01: local standard-library simulation, no real calendar provider."""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc


def inspect_local(local_iso: str, timezone: str) -> dict:
    naive = dt.datetime.fromisoformat(local_iso)
    if naive.tzinfo is not None:
        raise ValueError('Input must be a naive local datetime')
    zone = ZoneInfo(timezone)
    candidates = []
    for fold in (0, 1):
        local = naive.replace(tzinfo=zone, fold=fold)
        instant = local.astimezone(UTC)
        back = instant.astimezone(zone)
        if back.replace(tzinfo=None) == naive and back.fold == fold:
            candidates.append({
                'fold': fold,
                'utc': instant.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'utc_offset_minutes': int(local.utcoffset().total_seconds() / 60),
            })
    status = {0: 'NONEXISTENT', 1: 'UNAMBIGUOUS', 2: 'AMBIGUOUS'}[len(candidates)]
    # Example of a permissive conversion: it silently chooses fold=0.
    permissive = naive.replace(tzinfo=zone, fold=0).astimezone(UTC)
    return {
        'timezone': timezone,
        'local_iso': local_iso,
        'status': status,
        'valid_utc_candidates': candidates,
        'permissive_fold0_utc': permissive.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'guard_action': 'ACCEPT' if status == 'UNAMBIGUOUS' else 'REQUEST_CLARIFICATION',
    }


def evidence() -> dict:
    cases = [
        ('fall_repeated_hour', '2026-11-01T01:30:00', 'America/Los_Angeles'),
        ('spring_skipped_hour', '2026-03-08T02:30:00', 'America/Los_Angeles'),
        ('ordinary_hour', '2026-10-30T09:00:00', 'America/Los_Angeles'),
        ('after_fall_transition', '2026-11-01T03:00:00', 'America/Los_Angeles'),
    ]
    return {
        'schema_version': '1.0',
        'experiment_id': 'NINFA-S01',
        'experiment_type': 'OFFLINE_LOCAL_SIMULATION',
        'provider_calendar_api_tested': False,
        'ai_agent_tested': False,
        'tzdb_version': 'system timezone database (not pinned)',
        'runtime': f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}',
        'limitations': [
            'This tests Python zoneinfo conversion behavior, not Google Calendar, Outlook or an actual scheduling integration.',
            'No user meeting was scheduled or changed.',
            'Time-zone database rules can evolve; rerun if tzdb changes.',
        ],
        'cases': [{'case_id': case, **inspect_local(local, zone)} for case, local, zone in cases],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, help='Optional JSON evidence file')
    args = parser.parse_args()
    data = evidence()
    result = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result, encoding='utf-8')
    print(result, end='')


if __name__ == '__main__':
    main()
