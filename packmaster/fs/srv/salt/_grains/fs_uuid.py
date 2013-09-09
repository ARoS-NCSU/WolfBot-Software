import os

def fs_uuid():

    # blkid -t LABEL=rootfs -o value -s UUID
    rootfs_uuid = os.popen('blkid -t LABEL=rootfs -o value -s UUID').read()

    #return {'fs_uuid': {'rootfs': 'deadbeef-1234-5678'} }
    return {'fs_uuid': {'rootfs': rootfs_uuid} }
