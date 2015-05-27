# -*- coding: utf-8 -*-
import sys
import json
import time
import requests
import datetime

REPO_URI = 'http://{es_node}:9200/_snapshot/{repo}'


def create_s3_repo(node, repo, bucket):
    _sys_print('Creating S3 repository...')

    repository_config = {
        "type": "s3",
        "settings": {
            "bucket": bucket,
            "base_path": "elasticsearch_snapshots"
        }
    }

    r = requests.put(REPO_URI.format(es_node=node, repo=repo),
                     data=json.dumps(repository_config))

    result = r.json()
    assert r.status_code == 200, result
    if not result['acknowledged']:
        raise Exception(
            'Was not able to create s3 repository!\nReason: {}'.format(result))
        exit(1)
    _sys_print(' [OK]\n')


def poll_snapshot_status(snapshot_uri):
    status_uri = "{snapshot_uri}/_status".format(snapshot_uri=snapshot_uri)
    failure_count = 0
    sleep_time = 1
    print "Files:"
    counter = 0
    spinner = ['|', '/', '-', '\\']
    while True:
        r = requests.get(status_uri)

        if r.status_code == 200:
            snapshot_status = r.json()
            status = snapshot_status['snapshots'][0]['state']
            if status == 'STARTED':
                stats = snapshot_status['snapshots'][0]['stats']
                _sys_print(
                    '\r{}/{} '.format(
                        stats['processed_files'], stats['number_of_files']))
            elif status == 'SUCCESS':
                return print_success_message(snapshot_status)
            else:
                raise Exception('Bad snapshot status: {}'.format(r.json()))
        else:
            failure_count += 1
            sleep_time = sleep_time * 2

        if failure_count > 10:
            raise Exception(
                'Bad status code {} {}'.format(r.status_code, r.content))
        counter += 1
        _sys_print(spinner[counter % len(spinner)])
        time.sleep(sleep_time)


def create_snapshot(node, repo):
    date_stamp = datetime.datetime.now().date().strftime('%Y%m%d')
    _sys_print('Creating snapshot for {} ...'.format(date_stamp))

    snapshot_uri = '{repo}/snapshot_{date}'.format(
        repo=REPO_URI.format(es_node=node, repo=repo), date=date_stamp)

    r = requests.put(snapshot_uri)

    result = r.json()
    assert r.status_code == 200, result

    if not result['accepted']:
        raise Exception('Snapshot Failed\nReason: {}'.format(result))

    _sys_print(' [OK]\n')

    poll_snapshot_status(snapshot_uri)


def print_success_message(snapshot_status):
    stats = snapshot_status['snapshots'][0]['stats']
    shard_stats = snapshot_status['snapshots'][0]['shards_stats']
    print '\n'
    print '-'*80
    print 'Stats: Files: {}/{}; Shards - {}/{}; Duration - {}s'.format(
        stats['processed_files'], stats['number_of_files'],
        shard_stats['done'], shard_stats['total'],
        stats['time_in_millis']/100)
    print '-'*80


def _sys_print(m):
    sys.stdout.write(m)
    sys.stdout.flush()
