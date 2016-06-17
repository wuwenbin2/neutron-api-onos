import os

from charmhelpers.fetch import (
    apt_install,
    filter_installed_packages,
)

from charmhelpers.core.host import (
    service_restart,
)

from subprocess import check_call

from charmhelpers.contrib.openstack.utils import os_release

NEUTRON_CONF_DIR = "/etc/neutron"
NEUTRON_CONF = '%s/neutron.conf' % NEUTRON_CONF_DIR
ML2_CONF = '%s/plugins/ml2/ml2_conf.ini' % NEUTRON_CONF_DIR

# Packages to be installed by charm.
def install_packages(servicename):
    if os_release('neutron-common') >= 'kilo':
        output = os.popen('pip install networking-onos')
        print output.read()
    pkgs = ['neutron-common', 'neutron-plugin-ml2']
    pkgs = filter_installed_packages(pkgs)
    apt_install(pkgs, fatal=True)
    update_config("")

def update_config(servicename):
    check_call("sudo neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head",shell=True)
    service_restart('neutron-server')
