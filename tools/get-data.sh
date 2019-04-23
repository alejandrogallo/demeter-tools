#! /usr/bin/env bash
set -u

source $1

mkdir -p $folder

for query in ${queries[@]}; do
  echo -e "\x1b[32m=== $query ===\x1b[0m"
  yamlfile="$folder/${query}.yaml"
  csvfile="$folder/${query}.csv"
  [[ ! -f ${yamlfile} ]] &&
  papis explore crossref \
    -q "$query" -s relevance -f type journal-article -m ${max} \
    export --format yaml -o "${yamlfile}"
  [[ ! -f ${csvfile} ]] && {
    echo "Creating csvfile ${csvfile}" 
    ./tools/to-csv.py "${yamlfile}" > "${csvfile}"
  }
  echo "Creating xlsxfile" 
  ./tools/csv-to-xlsx.py "${csvfile}"
done
