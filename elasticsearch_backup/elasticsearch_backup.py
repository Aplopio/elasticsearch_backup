# -*- coding: utf-8 -*-
import sys
import json
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


def create_snapshot(node, repo):
    date_stamp = datetime.datetime.now().date().strftime('%Y%m%d')
    _sys_print('Creating snapshot for {} ...'.format(date_stamp))

    snapshot_uri = '{repo}/snapshot_{date}?wait_for_completion=true'.format(
        repo=REPO_URI.format(es_node=node, repo=repo), date=date_stamp)

    r = requests.put(snapshot_uri)

    result = r.json()
    assert r.status_code == 200, result
    if result['snapshot']['state'] != 'SUCCESS':
        raise Exception('Snapshot Failed\nReason: {}'.format(result))

    _sys_print(' [OK]\n')
    print '-'*80
    print 'Stats: Shards - {}/{}; Duration - {}s'.format(
        result['snapshot']['shards']['successful'], result['snapshot']['shards']['total'],
        result['snapshot']['duration_in_millis']/100)
    print '-'*80


def _sys_print(m):
    sys.stdout.write(m)
    sys.stdout.flush()
