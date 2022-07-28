#!/bin/bash
cwd=$(cd $(dirname $0) && pwd)
cd $cwd

source $cwd/../../functions/initial
source ./INPUT

log_file=$cwd/LOG
result_file=$cwd/RESULT
touch $log_file
touch $result_file

# gadmin config set RESTPP.Factory.DefaultQueryTimeoutSec 600
# gadmin config apply -y
# gadmin restart -y all

sleep 5

for i in "${HOP_LIST[@]}"
do
    # cd $cwd/"$i"-hop/
    echo "Install the $i-hop queries"
    for k in {1..50}
    do
        gsql -g ldbc_snb $cwd/"$i"-hop/test"$k".gsql
    done
    gsql install query -force all

    echo "Compute cardinality and histogram"
    python3 statistics.py -card -hist tee -a RESULT
    for j in {1..3}
    do  
        echo "Do $i-hop $j-iteration"
        # chmod 777 -R $cwd/"$i"-hop/exefile
        # echo "Run $i-hop queries' bash file"
        # source $cwd/"$i"-hop/exefile |& tee -a RESULT 
        # echo "$j-th iteration of $i-hop query test finished"

        echo "Run the $i-hop queries with optimizer"
        for k in {1..50}
        do
            echo "run query $k with optimizer" |& tee -a "$i"hop_query"$j".txt 
            (time gsql -g ldbc_snb "set cost_opt = true run query test$i()") |& tee -a "$i"hop_query"$j".txt
        done

        echo "Run the $i-hop queries without optimizer"
        for k in {1..50}
        do
            echo "run query $k without optimizer" |& tee -a "$i"hop_query"$j".txt 
            (time gsql -g ldbc_snb "set cost_opt = false run query test$i()") |& tee -a "$i"hop_query"$j".txt
        done
        echo "Done $i-hop $j-iteration"
    done
    gsql drop query all
    echo "$i query test DONE"
done