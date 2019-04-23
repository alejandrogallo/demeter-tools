#! /usr/bin/env bash
set -eu

source $1

[[ -d $folder ]]

for query in ${queries[@]}; do
  echo -e "\x1b[32m=== $query ===\x1b[0m"

  f="$folder/$query.csv"
  test -f $f

  cat $f                   |
  awk -F '\t' '{print $3}' |
  sort                     |
  uniq -c                  |
  tee years.csv



done
