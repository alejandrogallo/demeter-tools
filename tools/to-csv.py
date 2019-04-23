#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import sys
import re

yamlfile = sys.argv[1]
assert(yamlfile.endswith('.yaml'))
cleanre = re.compile(r'[\n\r]')
cleantab = re.compile(r'[\t"]')

fmt = (
    "{title}{s}{author}{s}{year}{s}{abstract}{s}{url}{s}"
    "{doi}{s}{affiliations}")

separator = '\t'

print(fmt.format(
    s=separator, title='title', author='author',
    year='year', abstract='abstract', url='url',
    doi='doi', affiliations='affiliations'))

with open(yamlfile) as fd:
    papers = yaml.load_all(fd)
    for p in papers:
        string = fmt.format(
            s=separator,
            title=cleantab.sub(' ', p.get('title', 'None')),
            doi=cleantab.sub(' ', p.get('doi', 'None')),
            author=cleantab.sub(' ', p.get('author', 'None')),
            url=cleantab.sub(' ', p.get('url', 'None')),
            year=cleantab.sub(' ', str(p.get('year', 'None'))),
            abstract=cleantab.sub(' ', p.get('abstract', 'None')),
            affiliations=cleantab.sub(' ', separator.join(
                a['affiliation'][0]['name'] if a.get('affiliation') else ''
                for a in p.get('author_list', [])
            ))
        )
        print(cleanre.sub(' ', string))
