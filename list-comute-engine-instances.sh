#!/bin/bash
# Script to retrieve compute engine details.
 
echo "PROJECT NAME, INSTANCE NAME , ZONE , MACHINE-TYPE , OPERATING SYSTEM , CPU , MEMORY , DISK SIZE, INTERNAL IP, EXTERNAL IP, HOSTNAME, STATUS, ZONE, STATE, FAILURE REASON" > compute-engine-details.csv
#prjs=( $(gcloud projects list | tail -n +2 | awk {'print $1'}))
#read -p "Enter the txt file containing the list of project: " projects 
for i in $(gcloud projects list --format="value(project_id)")
    do
        echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" >> list.txt
        echo "Setting Project: $i" >> list.txt
        echo $(gcloud config set project $i)
        echo "Checking if the compute API is enabled"
        iscomputeapienabled=$(gcloud services list --enabled --filter="name:compute.googleapis.com" --format="value(name)")
        scomputeapienabled=$(gcloud services list --enabled --filter="name:compute.googleapis.com" --format="value(name)")
        isconfigapienabled=$(gcloud services list --enabled --filter="name:osconfig.googleapis.com" --format="value(name)")
        if [[ ! -z "$isconfigapienabled" ]]
        then
            patchid=$(gcloud compute os-config patch-jobs list --limit 1 --format="value(ID)")
        else
            patchid=0
            
        fi
    echo $1,$2,$3,$4,$5
        if [ -z "$iscomputeapienabled" ] ; then continue; else echo $(gcloud compute instances list --format="value(name,zone,status)" | awk '{print $1,$2,$3}' | tail -n +2| while read line; do echo "$i $line $patchid"; done |xargs -n5 sh -c 'python3  retrieve-compute-engine-details.py $1 $2 $3 $4 $5 >> compute-engine-details.csv' sh); fi
    done
