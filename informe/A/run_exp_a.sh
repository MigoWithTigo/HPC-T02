#!/bin/bash
REPS=${1:-10}
OUTFILE="results_exp_a.csv"
echo "n,rep,tiempo_ms,checksum" > "$OUTFILE"

for n in 2048 1024 512 256 128 64 32; do
    for rep in $(seq 1 $REPS); do
        line=$(./serial 2048 $n)
        t=$(echo "$line" | grep -oP 'tiempo=\K[0-9.]+')
        cs=$(echo "$line" | grep -oP 'checksum=\K[-0-9.]+')
        echo "$n,$rep,$t,$cs" >> "$OUTFILE"
        echo "n=$n rep=$rep t=$t cs=$cs"
    done
done
echo "=== DONE ==="
