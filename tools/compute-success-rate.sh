#! /usr/bin/env bash

set -eu


for folder in ${@}; do

  echo -e "\x1b[32m == $folder ==\x1b[0m"

  query=$(basename ${folder%-missing})
  new=${folder}/new.csv
  failed=${folder}/failed.csv

  let new_sum=$(($(wc -l $new | cut -f1 -d' ')-1))
  let failed_sum=$(($(wc -l $failed | cut -f1 -d' ')-1))

  let total=new_sum+failed_sum
  error_percentage=$(
    python -c "print(float($failed_sum)/($new_sum+$failed_sum) * 100)")

  echo $query $error_percentage

done
