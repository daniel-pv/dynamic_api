import os.path
import logging
import json
from entities.endpoint import ApiFile, Api, EndPoint
from provider.originAdapter import OriginAdapter
from provider.destinyAdapter import DestinyAdapter
from xmlrpc.client import boolean
from pathlib import Path
script_dir = os.path.dirname(__file__)


class FileProvider(OriginAdapter, DestinyAdapter):
    def __init__(self, file_name='', folder_path=''):
        if file_name == '':
            file_name = 'source.json'
        if folder_path == '':
            folder_path = '{}/apps'.format(script_dir[:-len('provider')])

        self._file_path = None
        super().__init__(source_path=folder_path, source_name=file_name)

    @property
    def file_path(self):
        return '{}/{}'.format(self.source_path, self.source_name)

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    def read(self) -> ApiFile:
        # Load file to  cast to python dataclass
        json_source = self.load_file()
        json_api_file = json.loads(json_source)
        
        return self.cast(json_api_file)

    def write(self, api_file: ApiFile) -> None:
        # Write data to endpoint file
        #self.source_name = '{}.py'.format(api_file.api_file_name)

        if not self.exists('{}/{}.py'.format(self.source_path, api_file.api_file_name)):
            pass

        for api in api_file.apis:
            to_write_lines = self.get_api_lines(api)
            self.source_name = '{}.py'.format(api.api_name)
            if self.write_file(to_write_lines):
                logging.info('New file[Name:{} created!]'.format(api.api_file_name))
                to_append_lines = self.get_api_file_lines(api.api_name, api_file.api_file_name)
                self.source_name = '{}.py'.format(api.api_file_name)
                self.write_file(to_append_lines, 'a')
            else:
                logging.error('Something failed at write file[Name:{}!]'.format(api.api_file_name))

    def exists(self, source_name: str = '') -> boolean:
        if source_name == '':
            source_name = '{}/{}'.format(self.source_path, self.source_name)

        return os.path.exists(source_name)

# region Helpers
    # region Write File
    def write_file(self, lines: list, mode='w') -> boolean:
        written = False
        if not self.exists(self.file_path):
            logging.info('File was not found in directory!')
            logging.info(
                'A new file[Name:{}] will be created!'
                .format(self.source_name))
        else:
            logging.info('File was found in directory!')
            logging.info(
                'File[Name:{}]  will be overwrite!'
                .format(self.source_name))

        with open(self.file_path, mode) as file:
            file.writelines(line + '\n' for line in lines)
            written = True

        return written
    # endregion

    # region Read File
    def load_file(self) -> str:
        json = ''

        if self.exists(self.file_path):
            with open(self.file_path) as file:
                json = file.read()
        else:
            logging.error('File was not found in directory!')

        return json
    # endregion

    # region Cast methods
    def cast(self, json_api):
        try:
            api_file = {}
            _api_file = ApiFile(
                port=json_api['port'],
                host=json_api['host'],
                variables=json_api['variables'],
                imports=json_api['imports'],
                api_file_name=json_api['api_file_name'],
                apis=[]
            )

            _apis = []
            for api in json_api['apis']:
                _api = Api(
                    api_file_name=json_api['api_file_name'],
                    api_name=api['api_name'],
                    main_api=True if api['main_api'] == 1 else False,
                    endpoints=[]
                )
                _endpoints = []
                for endpoint in api['endpoints']:
                    _endpoint = EndPoint(
                        api_name=api['api_name'],
                        method=endpoint['method'],
                        name=endpoint['name'],
                        params=endpoint['params'],
                        payload=endpoint['payload'],
                        route=endpoint['route'],
                    )
                    _endpoints.append(_endpoint)
                _api.endpoints = _endpoints

                _apis.append(_api)
            _api_file.apis = _apis
            api_file = _api_file
        except Exception:
            logging.error('Json content does not have valid API information.')

        return api_file

    def get_api_file_lines(self, api_name: str, api_file_name: str):
        # To apen to file
        write_lines = ['\n']
        write_lines.append('subapp = importlib.import_module("{}", "{}")'.format(api_name, api_file_name))
        write_lines.append('{}.include_router(subapp.router)'.format(api_file_name))

        return write_lines

    def get_api_lines(self, api: Api):
        # start of file
        write_lines = [
            'from fastapi import APIRouter, status',
            'from model import *',
            '\n',
            'router = APIRouter()']
        
        write_lines.append('\n')
        for endpoint in api.endpoints:
            write_lines.extend(self.get_lines(endpoint, api))
        write_lines.append('\n')

        return write_lines

    def get_lines(self, endpoint: EndPoint, api: Api):
        write_lines = []
        write_lines = [
            '#method={}'.format(endpoint.method.upper()),
            self.build_header(endpoint=endpoint, api=api),
            self.build_definition(endpoint=endpoint),
            self.build_return(endpoint=endpoint)]

        return write_lines

    def build_header(self, endpoint: EndPoint, api: Api):
        return '@router.{method}(\"/{route}\", tags=["{tag}"])'.format(
            method=endpoint.method,
            route=endpoint.route,
            tag=api.api_name)

    def build_definition(self, endpoint: EndPoint):
        return 'async def {name}({params}):'.format(
            name=endpoint.name,
            params=endpoint.params)

    def build_return(self, endpoint: EndPoint):
        payload = '{"Hello world!"}' if endpoint.payload == '' else endpoint.payload
        return '    return {}'.format(payload)
    # endregion
    def rchop(s, suffix):
        if suffix and s.endswith(suffix):
            return s[:-len(suffix)]
        return s
# endregion
