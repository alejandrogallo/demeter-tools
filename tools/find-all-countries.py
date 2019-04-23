#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import click
import colorama
import logging
from multiprocessing.pool import ThreadPool
import functools


def get_countries(args):
    """Find countries in yaml file f"""
    assert(len(args) == 2)
    f = args[0]
    year = args[1]
    logging.info('Processing {}'.format(f))
    iso_codes = set()
    with open(f) as fd:
        docs = list(yaml.load_all(fd))
    N = len(docs)
    for K, d in enumerate(docs):
        logging.info(
            "{c.Fore.CYAN}{K}/{N}. "
            "Trying {c.Fore.YELLOW}{0}{c.Style.RESET_ALL}"
            .format(d.get('doi'), K=K, N=N, c=colorama))
        if 'countries' not in d:
            raise Exception('No country found for {doi} in {f}'
                            .format(doi=d.get('doi', 'no doi'), f=f))
        else:
            if year and 'year' in d and year != int(d['year']):
                continue
            iso_codes |= set(d['countries'])

    return iso_codes


@click.command()
@click.argument('input_yaml_files', nargs=-1, type=click.Path(exists=True))
@click.option('--log-out', default='log.out')
@click.option('--threads', default=4, type=int)
@click.option('--year', type=int, default=None)
@click.option('--out', default='countries.yaml')
def main(input_yaml_files, log_out, year, threads, out):
    logging.basicConfig(filename=log_out, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Running on {} threads'.format(threads))
    pool = ThreadPool(threads)
    result = pool.map(get_countries, [(f, year) for f in input_yaml_files])
    pool.close()
    pool.join()
    iso_codes = sorted(functools.reduce(lambda x, y: x | y, result))

    with open(out, "w+") as fd:
        logging.info('Dumping in {0}'.format(out))
        yaml.dump(iso_codes, fd)


if __name__ == "__main__":
    main()
