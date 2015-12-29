#!/bin/sh

#channel="mu"
channel="el"
masses="800 1000 1200 1400 1600 1800 2000 2500 3000 3500 4000 4500"

for mass in $masses;
do
  left="2ljets/new_list_BulkGrav_M-${mass}_${channel}Channel.txt"
  right="../sync_${channel}/BulkGravToZZToZlepZhad_narrow_${mass}/XZZDumpEvtList/eventlist.txt"
  echo "# ${channel} channel, M ${mass} :"
  diff -w ${left} ${right}
done


