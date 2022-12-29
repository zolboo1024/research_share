#!/bin/bash
pcaps="/home/zolboo/whatsapp/whatsapp/andr/traffic/pcaps/"
tran="/home/zolboo/whatsapp/whatsapp/andr/traffic/tran/"
apps=(dis tea tel sig wha mes)
for app in ${apps[@]}; do
    pcap_file=${pcaps}${app}/$1/${app}_$1_hourlong_filtered.pcap
    dest_file=${tran}${app}_$1
    echo tranalyzer -r ${pcap_file} -w ${dest_file}tcp
    tranalyzer -r ${pcap_file} -w ${dest_file}tcp
done