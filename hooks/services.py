from functools import partial
from charmhelpers.core import hookenv
from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers
from charmhelpers.contrib.openstack.templating import get_loader
from charmhelpers.contrib.openstack.utils import os_release, remote_restart

import onos_package
import onos_relation


def manage():
    config = hookenv.config()
    release = os_release('neutron-common')
    manager = ServiceManager([
        # onos services setup
        {
            'service': 'onos-setup',
            'data_ready': [
                onos_package.install_packages,
            ],
            'provided_data': [
                onos_relation.BuildSDNRelation(),
            ],
        },
        {
            'service': 'api-render',
            'required_data': [
                onos_relation.ONOSControllerRelation(),
                config,
                onos_relation.ConfigTranslation(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='ml2_conf.ini',
                    template_loader=get_loader('templates/', release),
                    target='/etc/neutron/plugins/ml2/ml2_conf.ini',
                    on_change_action=(partial(remote_restart,
                                              'neutron-plugin-api-subordinate',
                                              'neutron-server')),
                ),
            ],
        },
    ])
    manager.manage()
