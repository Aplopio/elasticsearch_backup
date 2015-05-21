# -*- coding: utf-8 -*-
import yaml
import click

import elasticsearch_backup


@click.command()
@click.option('--config', default='/etc/elastic_search_backup/config.yml',
              help="Configuration for elastic search backup.")
def main(config):
    node, repo, bucket = parse_config(config_file=config)
    print "-"*80
    print "node: {}\nrepo: {}\nbucket: {}".format(node, repo, bucket)
    print "-"*80
    elasticsearch_backup.create_s3_repo(node=node, repo=repo, bucket=bucket)
    elasticsearch_backup.create_snapshot(node=node, repo=repo)


def parse_config(config_file):
    with open(config_file) as c:
        conf = yaml.load(c)
    return conf['node']['host'], conf['repo'], conf['bucket']
