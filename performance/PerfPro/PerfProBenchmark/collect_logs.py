import os
import sys
import shutil
import yaml
from datetime import datetime as DT
now=DT.now()
time_string = now.strftime("%m-%d-%Y-%H-%M-%S")
conf_yaml = open(sys.argv[1])
parse_conf = yaml.load(conf_yaml , Loader=yaml.FullLoader)

'''Below configuration parameters are collected from config.yml file'''
nfs_server=parse_conf.get('NFS_SERVER')
nfs_export=parse_conf.get('NFS_EXPORT')
mount_point=parse_conf.get('NFS_MOUNT_POINT')
log_dest=parse_conf.get('NFS_FOLDER')

source_zip_prefix='benchmark_'
log_source='benchmark.log'

class collect_logs:
    '''Mounts the NFS export on the mountpoint to copy the collected logs'''    
    def mount_nfs(self):
        os.system('mkdir '+mount_point)
        os.system('mount '+nfs_server+':'+nfs_export+' '+mount_point)
        return('Export mounted')

    '''Create the Zipped copy of recently collected logs by benchmarking tool'''
    def zip_logs(self):
        os.system(' tar -cvzf '+source_zip_prefix+time_string+'.tar.gz'+' '+log_source)
        return('logs collected and zipped as '+source_zip_prefix+time_string+'.tar.gz')
   
    '''Copy the Zipped copy to NFS Repo'''
    def copy_logs(self):
        shutil.copy(source_zip_prefix+time_string+'.tar.gz', mount_point+log_dest)
        return('Logs copied to NFS Repo.')

    '''Show the contents of NFS Repo for verification of code'''
    def show_logs(self):
        return(os.listdir(mount_point+log_dest))

    '''Unmounts the NFS export and deleted the mountpoint'''
    def unmount_nfs(self):
        os.system('umount -l '+mount_point)
        os.system('rmdir '+mount_point)
        return('Exiting after log collection.')

logs=collect_logs()
print(logs.mount_nfs())
print(logs.zip_logs())
print(logs.copy_logs())
print(logs.show_logs())
print(logs.unmount_nfs())
