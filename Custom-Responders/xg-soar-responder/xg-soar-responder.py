#!/usr/bin/python3
# encoding: utf-8

from cortexutils.responder import Responder
import requests

class SoarConnector(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.xg_soar_connector_url = self.get_param('config.xg_soar_connector_url', None, 'No Connector URL Set')
        self.xg_soar_connector_token = self.get_param('config.xg_soar_connector_token', None, 'No Token set')
        self.observable = self.get_param('data.data', None, 'Data is empty')
        self.observable_type = self.get_param('data.dataType', None, 'Data type is empty')


    def run(self):
        Responder.run(self)

        h = {
            'Authorization': f'Bearer {self.xg_soar_connector_token}'
        }

        if self.observable_type == 'fqdn' or self.observable_type == 'domain':
            r = requests.get(f'{self.xg_soar_connector_url}/api/blacklistfqdn/add/{self.observable}', headers=h)

        elif self.observable_type == 'ip':
            r = requests.get(f'{self.xg_soar_connector_url}/api/blacklistip/add/{self.observable}', headers=h)

        if r.status_code == 200:
            self.report({'message': f'{self.observable} successfully pushed to SOPHOS SOAR Connector'})

        else:
            self.error({'message': r.status_code})

    def operations(self, raw):
        return [self.build_operation('AddTagToArtifact', tag=f'{self.observable_type} successfully pushed to SOPHOS SOAR Connector'), \
                self.build_operation('AddTagToCase', tag=f'{self.observable_type} successfully pushed to SOPHOS SOAR Connector')]

if __name__ == '__main__':
    SoarConnector().run()
