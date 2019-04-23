#! /usr/bin/env bash
set -eu

source $1
year=$2

[[ -d $folder ]] && [[ -d $analysis_folder ]]

main_out_folder=${analysis_folder}/country-tables/${year}/
country_file=${main_out_folder}/countries.yaml
country_file="analysis/5/country-list.yaml"

mkdir -p ${main_out_folder}

# Use a country file with all files, otherwise later is difficult to add
#
#[[ -f ${country_file} ]] ||
#./tools/find-all-countries.py \
  #$folder/*-missing/countries/new.yaml \
  #--threads 10 \
  #--year $year \
  #--out ${country_file} &&
#echo "$country_file already exists, not computing it again..."

for query in ${queries[@]}; do
  echo -e "\x1b[32m=== $query ===\x1b[0m"

  outfolder="${main_out_folder}/${query}"

  #[[ -d ${outfolder} ]] && {
    #echo -e "\x1b[31m $outfolder exists, remove if you want to process \x1b[0m"
    #continue
  #}

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
    --year $year \
    --country-file ${country_file} \
    --out ${out_yaml}

  echo "Creating csvfile ${out_csv}"
  sed "s/: \+/\t/g; 1icountry_iso_code\thits\tdois" "${out_yaml}" > "${out_csv}"

done
