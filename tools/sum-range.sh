#! /usr/bin/env bash
#vim-run: bash % 2012 2019

set -eu

start=$1
end=$2
years=($(seq $start $end))
nyears=${#years[@]}
__seq=($(seq 2 $(($nyears+1))))
sumseq=$(echo ${__seq[@]/#/$} | sed "s/ /+/g")
queries=($(ls -d $start/* | xargs -n1 basename))
outfolder="$start-$end"
generalcsv="$outfolder/general.csv"

echo ${years[@]}

mkdir -p $outfolder

echo -e "query\tcountries" > $generalcsv

for query in ${queries[@]}; do

  mkdir -p $outfolder/${query}
  tablecsv="$outfolder/${query}/table-per-year.csv"
  tablesimpcsv="$outfolder/${query}/table-summed-simplified.csv"

  {
    tables=${years[@]/%/\/$query/table.csv}
    paste \
      <(awk '{print $1}' "$start/$query/table.csv") \
      <(paste ${tables[@]} | sed "s/[a-z-]//ig")
  } |
  sed "s/\s\+/\t/g" |
  sed 1d > $tablecsv

  set -x
  awk '{print $1, '${sumseq}'}' $tablecsv |
  sed "/\s0$/d" > $tablesimpcsv

  echo -e "$query\t$(awk '{print $1}' $tablesimpcsv | tr '\n' '\t')" >> \
    $generalcsv

done


