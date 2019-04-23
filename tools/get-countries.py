#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import doi
import countrynames
import yaml
import click
import functools
import operator
import colorama
import time
import logging


def has_affiliation(doc):
    if 'author_list' in doc and doc['author_list']:
        affs = [
            aff.get('name')
            for a in doc['author_list']
            for aff in a.get('affiliation', [])
            if aff and
            isinstance(aff, dict) and
            aff.get('name')
        ]
        return affs
    else:
        return False


@click.command()
@click.option('-f', type=click.Path(exists=True))
@click.option('--failed-out', default='failed.yaml')
@click.option('--new-out', default='new.yaml')
@click.option('--log-out', default='log.out')
def main(f, failed_out, new_out, log_out):
    logging.basicConfig(filename=log_out, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    new_docs = []
    failed_docs = []
    try:

        with open(f) as fd:
            docs = list(yaml.load_all(fd))
            N = len(docs)
            for K, d in enumerate(docs):
                url = d.get('url')
                affs = has_affiliation(d)
                success_rate = 100.0 - float(len(failed_docs)) / N * 100
                logging.info(
                    "{c.Fore.CYAN}[{s:.1f}%]: {K}/{N}. {t}>>"
                    "{c.Fore.YELLOW}Trying {0}{c.Style.RESET_ALL}"
                    .format(
                        url, s=success_rate,
                        K=K, N=N, t=time.ctime(), c=colorama))
                try:
                    if not affs:
                        raise Exception('No affiliations')
                    countries = list(filter(
                                    bool,
                                    [countrynames.to_code(aff, fuzzy=True)
                                     for aff in affs]))
                    if not countries:
                        raise Exception('No countries ({aff!s})'
                                .format(aff=affs))
                except Exception as e:
                    logging.info(
                            "{c.Fore.RED}\tFailed ({e})"
                            "{c.Style.RESET_ALL}"
                            .format(e=e,
                                c=colorama))
                    failed_docs.append(d)
                else:
                    logging.info(
                          "{c.Fore.GREEN}\tsuccess "
                          "{codes!s}\n"
                          "\t\t{affs!s}"
                          "{c.Style.RESET_ALL}"
                          .format(
                              d.get('url'),
                              codes=countries,
                              affs=affs,
                              c=colorama))
                    d['countries'] = countries
                    new_docs.append(d)

    except Exception as e:
        logging.error(e)
    finally:
        with open(failed_out, 'w+') as fd:
            logging.info('writing ' + failed_out)
            yaml.dump_all(
                list(failed_docs),
                fd,
                allow_unicode=True,
                default_flow_style=False)

        with open(new_out, 'w+') as fd:
            logging.info('writing '+ new_out)
            yaml.dump_all(
                list(new_docs),
                fd,
                allow_unicode=True,
                default_flow_style=False)


if __name__ == "__main__":
    main()
