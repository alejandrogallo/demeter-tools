#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import click
import colorama
import logging
import functools
import collections


@click.command()
@click.option('-f', type=click.Path(exists=True))
@click.option('--log-out', default='log.out')
@click.option('--country-file', required=True)
@click.option('--year', type=int, default=None)
@click.option('--out', required=True)
def main(f, log_out, year, country_file, out):
    logging.basicConfig(filename=log_out, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Processing {}'.format(f))

    with open(country_file) as fd:
        countries = list(yaml.load(fd))

    counter = collections.OrderedDict((c, 0) for c in countries)
    doi_counter = collections.OrderedDict((c, []) for c in countries)

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
                logging.info(
                    '::ignoring because of year {year}'.format(year=d['year']))
                continue
            for c in set(d['countries']):
                counter[c] += 1
                doi_counter[c].append(d['doi'])
                print(doi_counter)

    with open(out, "w+") as fd:
        logging.info('Dumping in {0}'.format(out))
        for c, v in counter.items():
            fd.write('{c}: {v}: {dois}\n'.format(
                c=c, v=v, dois='\t'.join(doi_counter[c])))

if __name__ == "__main__":
    main()
