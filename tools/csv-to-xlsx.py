#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import sys
import os


csvfile = sys.argv[1]
excelfile = csvfile.replace('.csv', '.xlsx')
name = os.path.basename(csvfile).replace('.csv', '').replace('+', ' ')


csvdata = pd.read_csv(csvfile, sep='\t', engine='c')
writer = pd.ExcelWriter(excelfile)
csvdata.to_excel(writer, sheet_name="{0:.30}".format(name), verbose=True)
writer.save()
