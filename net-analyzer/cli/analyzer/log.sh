DATE=$(date +%d-%m-%y)
TIME=$(date +%H:%M:%S)
LOG=$DATE-logs/$TIME.log

mkdir $DATE-logs
touch $LOG

for start in $(seq 0 5 255); do
    end=$((start+4))

    echo "Reporte $start - $end" >> $LOG

done