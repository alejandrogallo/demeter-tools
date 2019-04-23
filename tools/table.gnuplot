set terminal pdfcairo
set output "table.pdf"

#set border linewidth 1
#set title font "Helvetica, 20"
#set label font "Helvetica-Bold, 20"
#set key font "Helvetica-Bold, 15"
#set xlabel font "Helvetica, 20"
#set ylabel font "Helvetica, 20"
#set xtics  font "Helvetica, 10"
#set ytics  font "Helvetica, 10"

set style data histogram
set style histogram cluster
set style fill pattern border 0
set boxwidth 0.9

set ylabel "Hits"
set xlabel "Country number"

set title system("basename `pwd` | tr '+' ' '")
#set datafile separator ","

plot "table.csv" u 2:xticlabel(1) title 'asdf'
