# Script to retrieve compute engine details.
from pprint import pprint
 
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import subprocess
 
import re
import sys
import os
 
credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)
 
if (len(sys.argv)) >=3:
    project=sys.argv[1]
    instance = sys.argv[2]
    zone = sys.argv[3]
   status = sys.argv[4]
   patchid = sys.argv[5]
   pzone=''
   pstate=''
   preason=''
 
    # # Get instance details
    request = service.instances().get(project=project, zone=zone, instance=instance)
    response = request.execute()
 
    if patchid != 0:
        #Get the patch details for the current project
        compliance_response = subprocess.Popen('gcloud config set project {} && gcloud compute os-config patch-jobs list-instance-details {} --format="value(ZONE,STATE,FAILURE_REASON)" --filter="name:{}"'.format(project,patchid,instance), shell=True, stdout=subprocess.PIPE).stdout.read().decode('ascii')
       compliance_details = compliance_response.split()
        if len(compliance_details)>0:
           pzone = compliance_details[0]
            pstate = compliance_details[1]
           try:
                preason = compliance_details[2]
            except IndexError:
                preason = "N/A"
 
        
    #Get Hostname
    Hostname = instance.upper()
 
    # Get Internal IP
    InternalIP = '|'.join([i['networkIP'] for i in response['networkInterfaces']])
 
    # Get External IP
    ExternalIP = response['networkInterfaces'][0]['accessConfigs'][0]['natIP'] if 'accessConfigs' in response['networkInterfaces'][0] and 'natIP' in response['networkInterfaces'][0]['accessConfigs'][0] else 'Not Assigned'
    
    # Get machine type
    mtype = re.search(r'(.*)/(.*)', response['machineType']).group(2)
 
    # Get operating system name
    osu = response['disks'][0]['licenses'][0] if 'licenses' in response['disks'][0] else "N/A"
    os = re.search(r'(.*)/(.*)', osu).group(2)
 
    # Get disk size
    dsize = str(response['disks'][0]['diskSizeGb']) + ' GB'
 
    # Use machine type to get cpu count & memory size
    mrequest = service.machineTypes().get(project=project, zone=zone, machineType=mtype)
    mresponse = mrequest.execute()
 
    # Get cpu count
    cpu = mresponse['guestCpus']
 
    # Get memory size
    megabyte = mresponse['memoryMb']
    gigabyte = 1.0/1024
    memory = str(gigabyte * megabyte) + ' GB'
 
    print(f'{project},{instance},{zone},{mtype},{os},{cpu},{memory},{dsize},{InternalIP},{ExternalIP},{Hostname},{status},{pzone or "N/A"},{pstate or "N/A"},{preason or "N/A"}')
