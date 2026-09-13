
from ..utils.sessions import get_client
import time
import os

MBPS_TO_BYTES = 1_000_000 / 8


def start_task_execution(task_arn):
    ds = get_client('datasync')
    resp = ds.start_task_execution(TaskArn=task_arn)
    return resp['TaskExecutionArn']


def get_execution_status(execution_arn):
    ds = get_client('datasync')
    resp = ds.describe_task_execution(TaskExecutionArn=execution_arn)
    return {
        'status': resp['Status'],
        'files_prepared': resp.get('Result', {}).get('PrepareDuration'),
        'files_transferred': resp.get('FilesTransferred', 0),
        'bytes_transferred': resp.get('BytesTransferred', 0),
        'files_verified': resp.get('FilesVerified', 0),
        'errors': resp.get('FilesDeleted', 0),
        'result': resp.get('Result', {})
    }


def wait_for_execution(execution_arn, poll_seconds=60):
    terminal = {'SUCCESS', 'ERROR'}
    while True:
        info = get_execution_status(execution_arn)
        status = info['status']
        transferred_gb = info['bytes_transferred'] / 1024**3
        print(f"[{time.strftime('%H:%M:%S')}] {status} | {info['files_transferred']} files | {transferred_gb:.2f} GB")
        if status in terminal:
            return info
        time.sleep(poll_seconds)


def set_task_throttle(task_arn, bandwidth_mbps):
    ds = get_client('datasync')
    throttle = 0 if bandwidth_mbps == 0 else int(bandwidth_mbps * MBPS_TO_BYTES)
    ds.update_task(TaskArn=task_arn, Options={'BytesPerSecond': throttle})
    label = f'{bandwidth_mbps} Mbps' if throttle else 'unlimited'
    print(f'Task throttle updated to {label} ({throttle} bytes/sec)')


def lambda_handler(event, context):
    task_arn = os.getenv('DATASYNC_TASK_ARN')
    mode = event.get('mode', 'daytime')
    throttle_map = {'daytime': 500, 'overnight': 9000}
    bandwidth = throttle_map.get(mode, 500)
    set_task_throttle(task_arn, bandwidth)
    return {'statusCode': 200, 'bandwidth_mbps': bandwidth, 'mode': mode}


def monitor_nightly_transfers(task_arns, poll_seconds=60):
    started = time.time()
    execution_arns = [start_task_execution(t) for t in task_arns]
    terminal = {'SUCCESS', 'ERROR'}
    final = {}

    while len(final) < len(execution_arns):
        print('
Task Execution Summary')
        print('-' * 80)
        for arn in execution_arns:
            if arn in final:
                info = final[arn]
            else:
                info = get_execution_status(arn)
                if info['status'] in terminal:
                    final[arn] = info
            elapsed = round((time.time() - started) / 60, 1)
            gb = info['bytes_transferred'] / 1024**3
            print(f'{arn[-18:]:18} | {info["status"]:10} | {gb:8.2f} GB | {elapsed:6.1f} min')
        if len(final) == len(execution_arns):
            break
        time.sleep(poll_seconds)

    return final
