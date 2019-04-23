#! /usr/bin/env bash
set -eu

source $1

# where the countries are
country_file=$2

[[ -d $folder ]]

for query in ${queries[@]}; do
  echo -e "\x1b[32m=== $query ===\x1b[0m"

  outfolder="analysis/$folder/country-tables/${query}"

  [[ -d ${outfolder} ]] && {
    echo -e "\x1b[31m $outfolder exists, remove if you want to process \x1b[0m"
    continue
  }

  missingfolder="$folder/${query}-missing"
  [[ -d ${missingfolder} ]] || {
    echo -e "\x1b[31m $missingfolder does not exists\x1b[0m"
    continue
  }

  countryfolder="${missingfolder}/countries"
  [[ -d ${countryfolder} ]] || {
    echo -e "\x1b[31m $countryfolder does not exists\x1b[0m"
    continue
  }

  inyamlfile="${countryfolder}/new.yaml"
  [[ -f $inyamlfile ]] || {
    echo "ERROR file $inyamlfile not found"
    continue
  }

  out_yaml="${outfolder}/table.yaml"
  out_csv="${outfolder}/table.csv"
  out_xlsx="${outfolder}/table.csv"

  echo "== Creating outfolder: $outfolder"
  mkdir -p ${outfolder}
  ./tools/compute-country-table.py \
    -f $inyamlfile \
    --country-file ${country_file} \
    --out ${out_yaml}

  echo "Creating csvfile ${out_csv}"
  sed "s/: \+/\t/; 1icountry_iso_code,hits" "${out_yaml}" > "${out_csv}"

  echo "Creating xlsxfile ${out_xlsx}" 
  ./csv-to-xlsx.py "${out_csv}"

  exit 0

done
