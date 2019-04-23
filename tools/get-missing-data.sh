#! /usr/bin/env bash
set -u

source $1

mkdir -p $folder

for query in ${queries[@]}; do
  echo -e "\x1b[32m=== $query ===\x1b[0m"

  inyamlfile="$folder/${query}.yaml"
  [[ -f $inyamlfile ]] || {
    echo "ERROR file $inyamlfile not found"
    continue
  }

  outfolder="$folder/${query}-missing"
  [[ -d ${outfolder} ]] && {
    echo -e "\x1b[31m $outfolder exists, remove if you want to process \x1b[0m"
    continue
  }

  new_yaml="${outfolder}/new.yaml"
  new_csv="${outfolder}/new.csv"
  new_xlsx="${outfolder}/new.csv"
  failed_yaml="${outfolder}/failed.yaml"
  failed_csv="${outfolder}/failed.csv"
  failed_xlsx="${outfolder}/failed.csv"
  logfile="${outfolder}/log.out"

  mkdir -p ${outfolder}
  ./tools/get-missing.py \
    -f $inyamlfile \
    --failed-out ${failed_yaml} \
    --new-out ${new_yaml} \
    --log-out ${logfile}

  echo "Creating csvfile ${new_csv}"
  ./tools/to-csv.py "${new_yaml}" > "${new_csv}"
  echo "Creating xlsxfile ${new_xlsx}" 
  ./tools/csv-to-xlsx.py "${new_csv}"

  echo "Creating csvfile ${failed_csv}"
  ./tools/to-csv.py "${failed_yaml}" > "${failed_csv}"
  echo "Creating xlsxfile ${failed_xlsx}" 
  ./tools/csv-to-xlsx.py "${failed_csv}"

done
