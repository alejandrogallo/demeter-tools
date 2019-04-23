#! /usr/bin/env bash
set -u

get_affiliations_number(){
  csv=$1
  awk -F '\t' '{print $7 }' ${csv}   |
  sed "/^\s*$/d"  |
  sed "/^affiliations$/d"  |
  wc -l
}

source $1

mkdir -p $folder
outfile=${analysis_folder}/affiliations-data.csv

echo -e "query\tcrossref\tpapis\ttotal" > $outfile

for query in ${queries[@]}; do
  echo -e "\x1b[32m=== $query ===\x1b[0m"


  in_csv_file="$folder/${query}.csv"
  [[ -f $in_csv_file ]] || {
    echo "ERROR file $in_csv_file not found"
    continue
  }

  missing_csv_file="$folder/${query}-missing/new.csv"
  [[ -f $missing_csv_file ]] || {
    echo "ERROR file $missing_csv_file not found"
    continue
  }

  crossref_affs="$(get_affiliations_number $in_csv_file)"
  total_affs="$(get_affiliations_number $missing_csv_file)"
  papis_affs=$((total_affs - crossref_affs))

  echo -e "$query\t$crossref_affs\t${papis_affs}\t${total_affs}" |
  tee -a $outfile

done
