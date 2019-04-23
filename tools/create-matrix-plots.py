#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import click
import logging
import os
import csv
import functools
import collections
import math
import sys
logging.basicConfig(level=logging.DEBUG)


research_fields = [
{'name': 'PE',
'long_name': 'Biobased PE',
'queries': [
'polyethylene+biobased',
'polyethylene+biopolymer',
]},
{'name': 'PET',
'long_name': 'Biobased PET',
'queries': [
'polyethylene+terephtathalate+biobased',
'polyethylene+terephtathalate+biopolymer',
]},
{'name': 'PP',
'long_name': 'Biobased PP',
'queries': [
'polypropylene+biobased',
'polypropylene+biopolymer',
]},
{'name': 'PA',
'long_name': 'Biobased PA',
'queries': [
'polyamide+biobased',
'polyamide+biopolymer',
]},
{'name': 'PLA',
'long_name': 'PLA',
'queries': [
'polylactic+acid+biobased',
'polylactic+acid+biopolymer',
]},
{'name': 'PHB',
'long_name': 'PHB',
'queries': [
'polyhydroxybutyrate+biobased',
'polyhydroxybutyrate+biopolymer',
]},
{'name': 'TPS',
'long_name': 'TPS',
'queries': [
'thermoplastic+starch',
'thermoplastic+starch+biobased',
'thermoplastic+starch+biopolymer'
]},
{'name': 'PBAT',
'long_name': 'PBAT',
'queries': [
'polybutylene+adipate-co-terephthalate+biopolymer'
]},
{'name': 'PEF',
'long_name': 'PEF',
'queries': [
'polyethylenefuranoate+biobased',
'polyethylenefuranoate+biopolymer',
]},
{'name': 'PBS',
'long_name': 'PBS',
'queries': [
'polybutylene+succinate+biobased',
'polybutylene+succinate+biopolymer',
]},
]


@click.command()
@click.option(
    '-d', type=click.Path(exists=True),
    help='Directory with the queries and the countries')
@click.option('-f', help='Filename with the csv data')
@click.option('-l', help='List of lands')
@click.option('--od', help='Output directory')
@click.option('--delimiter', help='Delimiter for csv data', default='\t')
def main(d, f, l, od, delimiter):
    logging.info(d)
    logging.info(f)
    if not os.path.exists(od):
        os.makedirs(od)
    with open(l) as fd:
        lands = functools.reduce(lambda x, y: x + y, list(csv.reader(fd)))
    matrix_dimension = math.ceil(math.sqrt(len(lands)))
    logging.info('matrix dimension {0}'.format(matrix_dimension))

    for rf in research_fields:
        output_dir = os.path.join(od, rf['long_name'])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        table_files = [os.path.join(d, query, f) for query in rf["queries"]]
        assert all([os.path.exists(p) for p in table_files])

        result = collections.OrderedDict((_l, []) for _l in lands)
        #print(result)
        for table_file in table_files:
            logging.info(table_file)
            with open(table_file) as fd:
                data = list(csv.reader(fd, delimiter=delimiter))
                for _d in data:
                    result[_d[0]] += _d[2:]

        for _l in lands:
            result[_l] = list(set(result[_l]))

        csv_list = [[p[0], str(len(p[1]))] + p[1] for p in result.items() ]
        output_csv = os.path.join(output_dir, 'data.csv')
        logging.info("writting {}".format(output_csv))
        # print(csv_list)
        # sys.exit(1)
        with open(output_csv, "w+") as fd:
            csv_data = '\n'.join(delimiter.join(p) for p in csv_list)
            #print(csv_data)
            fd.write(csv_data)


if __name__ == "__main__":
    main()
