#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import doi
import papis.crossref
import papis.downloaders
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
@click.option('--failed-out')
@click.option('--new-out')
@click.option('--log-out')
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
                affs = has_affiliation(d)
                success_rate = 100.0 - float(len(failed_docs)) / N * 100
                if affs:
                    new_docs.append(d)
                    continue
                try:
                    url = doi.get_real_url_from_doi(d['doi'])
                    logging.info(
                        "{c.Fore.CYAN}[{s:.1f}%]: {K}/{N}. {t}>>"
                        "{c.Fore.YELLOW}Trying {0}{c.Style.RESET_ALL}"
                            .format(url, s=success_rate,
                                K=K, N=N, t=time.ctime(), c=colorama))
                    downs = papis.downloaders.get_matching_downloaders(url)
                    downs[0].fetch_data()
                    ctx = downs[0].ctx

                    affs = has_affiliation(ctx.data)
                    if affs:
                        d['author_list'] = ctx.data['author_list']
                    else:
                        raise Exception('No affiliations')
                except Exception as e:
                    d['_error_msg'] = str(e)
                    logging.info("{c.Fore.RED}\tFailed ({e}){c.Style.RESET_ALL}"
                          .format(e=e, c=colorama))
                    failed_docs.append(d)
                else:
                    logging.info("{c.Fore.GREEN}\tsuccess "
                          "{affs!s:.100}{c.Style.RESET_ALL}"
                          .format(url, affs=affs, c=colorama))
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
