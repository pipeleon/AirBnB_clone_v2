 #!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the web_static folder"""

from fabric.api import local
from datetime import datetime
from os.path import exists
env.hosts = ['34.138.186.79', '34.236.145.29']


def do_pack():
    """Creates a .tzg file"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        name_file = "versions/web_static_" + date + ".tgz"
        local("tar -czvf {} web_static".format(name_file))
        return name_file
    except:
        return None

def do_deploy(archive_path):
    """Deploys webserver content"""
    if not exists(archive_path):
        return False

    put(archive_path, '/tmp/')
    file_name = archive_path.split('.')[0].split('/')[1]
    d_folder = "/data/web_static/releases/{}".format(file_name)
    run('mkdir -p {}'.format(d_folder))
    run('tar -xzf /tmp/{}.tgz -C {}'.format(file_name, d_folder))
    run('rm /tmp/{}.tgz'.format(file_name))
    run('mv {}/web_static/* {}/'.format(d_folder, d_folder))
    run('rm -rf {}/web_static'.format(d_folder))
    run('rm -rf /data/web_static/current')
    run('ln -s {} /data/web_static/current'.format(d_folder))
    return True
