import json
from charmhelpers.core.services import helpers
from charmhelpers.core.hookenv import(
    config,
)

VXLAN = 'vxlan'
OVERLAY_NET_TYPES = [VXLAN]

class BuildSDNRelation(helpers.RelationContext):
    name = 'neutron-plugin-api-subordinate'
    interface = 'neutron-plugin-api-subordinate'

    def provide_data(self):

        neutron_config = {
            "neutron-api": {
                "/etc/neutron/neutron.conf": {
                    "sections": {
                        'DEFAULT': [
                        ],
                    }
                }
            }
        }
        relationinfos = {
            'neutron-plugin': 'onos',
            'core-plugin': 'neutron.plugins.ml2.plugin.Ml2Plugin',
            'neutron-plugin-config': '/etc/neutron/plugins/ml2/ml2_conf.ini',
            'service-plugins': 'onos_router',
            'subordinate_configuration': json.dumps(neutron_config),
        }
        return relationinfos


class ONOSControllerRelation(helpers.RelationContext):
    name = 'onos-controller'
    interface = 'onos-controller-api'

    def getdata(self):
        if self.get('onos-controller') and len(self['onos-controller']):
            return self['onos-controller'][0]
        else:
            return {}

    def get_data(self):
        super(ONOSControllerRelation, self).get_data()
        contoller = self.getdata()
        self['onos_ip'] = contoller.get('private-address')
        self['onos_port'] = contoller.get('port')
        self['onos_username'] = contoller.get('username')
        self['onos_password'] = contoller.get('password')

    def is_ready(self):
        if 'password' in self.getdata():
            return True
        else:
            return False


class ConfigTranslation(dict):
    def __init__(self):
        self['overlay_network_type'] = self.get_overlay_network_type()
        self['security_groups'] = config('security-groups')
    def get_overlay_network_type(self):
        overlay_networks = config('overlay-network-type').split()
        for overlay_net in overlay_networks:
            if overlay_net not in OVERLAY_NET_TYPES:
                raise ValueError('Unsupported overlay-network-type %s'
                                 % overlay_net)
        return ','.join(overlay_networks)
