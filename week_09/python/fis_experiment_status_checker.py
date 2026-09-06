"""
A04 - FIS Experiment Status Checker
Source: CDSAP1_ Migration Monitoring with Python — DMS Task Tracking and Snow Transfer Planning
"""

import boto3
from datetime import datetime

fis = boto3.client('fis', region_name='af-south-1')


def summarise_fis_experiments(max_results=10):
    """Print a summary of the most recent FIS experiments."""

    experiments = fis.list_experiments().get('experiments', [])

    print(f'Found {len(experiments)} experiments (showing up to {max_results}):')
    print('-' * 100)

    for exp in experiments[:max_results]:
        try:
            detail = fis.get_experiment(id=exp['id'])['experiment']

            short_id = exp['id'][-16:]
            template = detail.get('experimentTemplateId', 'unknown')
            state = detail.get('state', {}).get('status', 'unknown')

            start_time = detail.get('startTime')
            if start_time:
                start_time_str = start_time.strftime('%H:%M %Y-%m-%d')
            else:
                start_time_str = 'not started'

            stop_condition = (
                detail.get('stopConditions', [{}])[0].get('value', 'none')
            )

            print(f'ID: ...{short_id}')
            print(f'  Template ID : {template}')
            print(f'  State       : {state}')
            print(f'  Started     : {start_time_str}')
            print(f'  Stop Cond.  : {stop_condition}')
            print()

        except Exception as e:
            print(f'Failed to retrieve experiment {exp.get("id", "unknown")}: {e}')


if __name__ == '__main__':
    summarise_fis_experiments()
