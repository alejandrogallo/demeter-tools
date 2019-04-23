#! /usr/bin/env python
#vim-run: python3 % --start 2012 --end 2019
#vim-run: pdb3 % --start 2012 --end 2019
# -*- coding: utf-8 -*-

import os
import click
import csv


def get_cleaned_structure(structure):
    newstructure = []
    for s in structure:
        dois = list(set(s[2:]))
        if len(dois) != 0:
            newstructure.append([s[0], str(len(dois))] + dois)
    return newstructure[1:]


@click.command()
@click.option('--start', type=int)
@click.option('--end', type=int)
def main(start, end):
    mainoutfolder = "{start}-{end}".format(**locals())
    if not os.path.exists(mainoutfolder):
        os.makedirs(mainoutfolder)
    queries = os.listdir(str(start))
    years = range(start, end+1)
    for query in queries:
        outfolder = os.path.join(mainoutfolder, query)
        if not os.path.exists(outfolder): os.makedirs(outfolder)
        print(query)
        incsvfiles = [os.path.join(str(y), query, 'table.csv') for y in years]
        assert all((os.path.exists(f) for f in incsvfiles))
        outsttructure = []
        for incsv in incsvfiles:
            with open(incsv) as fd:
                data = list(csv.reader(fd, delimiter="\t"))
                if not outsttructure:
                    outsttructure = [[s for s in t if s] for t in data]
                else:
                    assert(len(data) == len(outsttructure))
                    for i in range(len(data)):
                        if not filter(bool, data[i][2:]):
                            continue
                        outsttructure[i].extend([s for s in data[i][2:] if s])
                        dois = outsttructure[i][2:]
                        outsttructure[i][1] = str(len(outsttructure[i][2:]))
        clean_structure = get_cleaned_structure(outsttructure)
        out_csv_table = os.path.join(outfolder, 'table.csv')
        with open(out_csv_table, "w+") as fd:
            fd.write('\n'.join('\t'.join(p) for p in clean_structure))


if __name__ == "__main__":
    main()
