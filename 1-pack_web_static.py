 #!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the web_static folder"""

from fabric.api import local
from datetime import datetime

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
