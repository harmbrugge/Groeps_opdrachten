#!/bin/sh
for host in [aib]* ; do echo $host; ssh $host 'mkdir -p /data/storage/tmp/Harm_Olivier/thema_06; cp -r /homes/hbrugge/Dropbox/Thema6/Genes_Plasmodium-falciparum.fa /data/storage/Harm_Olivier/thema_06'; done
for host in b* ; do echo $host; ssh $host 'mkdir -p /data/storage/tmp/Harm_Olivier/thema_06; cp -r /homes/hbrugge/Dropbox/Thema6/Genes_Plasmodium-falciparum.fa /data/storage/tmp/Harm_Olivier/thema_06'; done
for host in b* ; do echo $host; ssh $host 'chmod  777 /data/storage/tmp/Harm_Olivier/thema_06/plasmodium_db/*'; done
