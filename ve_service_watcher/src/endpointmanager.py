from provider.destinyAdapter import DestinyAdapter
from provider.originAdapter import OriginAdapter
import os
import subprocess
import sys
import logging


class EndpointManager:
    def __init__(
        self,
        destiny: DestinyAdapter,
        origin: OriginAdapter):
        self.destiny = destiny
        self.origin = origin

    def run(self):
        api_file = self.origin.read()
        self.destiny.write(api_file)
        if self.destiny.exists():
            logging.error('file[Name:{}] was not found!!!'.format(self.destiny.file_path))
        else:
            logging.info('file[Name:{}] will be launched!!!'.format(self.destiny.file_path))
            # run endpoint file in console
            os.system(
                'cmd /k "python \"{}\""'
                .format(self.destiny.file_path))

    def install(self, package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
