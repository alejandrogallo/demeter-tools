set -eu


queries=(
polyethylene+biobased
polyethylene+biopolymer
polyethylene+terephtathalate+biobased
polyethylene+terephtathalate+biopolymer
polypropylene+biobased
polypropylene+biopolymer
polyamide+biobased
polyamide+biopolymer
polylactic+acid+biobased
polylactic+acid+biopolymer
polyhydroxybutyrate+biobased
polyhydroxybutyrate+biopolymer
thermoplastic+starch
thermoplastic+starch+biobased
thermoplastic+starch+biopolymer
polybutylene+adipate-co-terephthalate+biopolymer
polyethylenefuranoate+biobased
polyethylenefuranoate+biopolymer
polybutylene+succinate+biobased
polybutylene+succinate+biopolymer
)

{
for query in ${queries[@]}; do
  folder="2012-2019/$query"
  test -d $folder
  test -f  $folder/table.csv
  awk -F "\t" '{print $1}' "$folder/table.csv"
done
} |
sort |
uniq
