from pathlib import Path
from csv import DictWriter
from google.cloud.compute import InstancesClient
from google.cloud.osconfig_v1.services.os_config_service import OsConfigServiceClient
 
if __name__ == '__main__':
    # breakpoint()
    header = [
        "PROJECT NAME", "INSTANCE NAME", "ZONE", "MACHINE-TYPE", "OPERATING SYSTEM",
        "CPU", "MEMORY", "DISK SIZE", "INTERNAL IP", "EXTERNAL IP", "HOSTNAME",
        "STATUS", "STATE", "FAILURE REASON"
    ]
    out_file = Path("./compute-engine-details.csv")
    out_file.touch()
    with open(out_file, "w") as fp, open("projects.txt") as projects:
        instances = InstancesClient()
        dict_writer = DictWriter(fp, fieldnames=header)
        dict_writer.writeheader()
        for project in projects.readlines():
            try:
                for zone, zone_instances in instances.aggregated_list(project=project):
                    for instance in zone_instances.instances:
                        # print(instance)
                        os_config_client = OsConfigServiceClient()
                        # breakpoint()
                        if not hasattr(instance, 'name'):
                            # print(f"Nothing in {zone=}")
                            continue
                        patch_list = os_config_client.list_patch_jobs(parent=f"projects/{project}")
                        patch = [i for i in patch_list.pages][0]
                        machine_type = instance.machine_type
                        dict_writer.writerow({
                            "PROJECT NAME": project,
                            "INSTANCE NAME": instance.name,
                            "ZONE": zone,
                            "MACHINE-TYPE": instance.machine_type.split("/")[-1],
                            "OPERATING SYSTEM": instance.disks[0].licenses[0].split("/")[-1],
                            "CPU": instance.cpu_platform,
                            "MEMORY": instance.disks[0].disk_size_gb,
                            "DISK SIZE": instance.disks[0].disk_size_gb,
                            "INTERNAL IP": instance.network_interfaces[0].network_i_p,
                            "EXTERNAL IP": instance.network_interfaces[0].access_configs[0].nat_i_p,
                            "HOSTNAME": instance.hostname,
                            "STATUS": instance.status.value,
                            "STATE": patch.pages[0].state if patch else "",
                            "FAILURE REASON": patch.pages[0].failure_reason if patch else ""
                        })
            except:
                continue