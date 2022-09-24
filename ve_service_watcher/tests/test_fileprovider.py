import pytest
import sys
import os
import json
import unittest
from unittest.mock import MagicMock, mock_open, patch
sys.path.insert(1, 'D:\\python\\workspace\\dynamic_api\\ve_service_watcher\\src')
from provider.fileprovider import FileProvider
from provider.sqliteProvider import SQLIteProvider
from entities.endpoint import EndPoint
from entities.endpoint import Api
from entities.endpoint import ApiFile
script_dir = os.path.dirname(__file__)
folder_path = """D:\\python\\workspace\\dynamic_api\\ve_dynamic_api\\"""


class TestEndpointManager:
    sqlProvider = SQLIteProvider()
    fileProvider = FileProvider('', '')

    def test_cast(self):
        json_api = """{
	"api_file_name": "endpoint_file",
	"imports": [],
	"variables": [],
	"apis": [
		{
			"api_name": "app",
			"main_api": 1,
			"endpoints": [
				{
					"method": "get",
					"route": "",
					"name": "root",
					"params": "",
					"payload": "{'Hello': 'World'}"
				}
			]
		}
	],
	"port": 8000,
	"host": "127.0.0.1"
}"""

        result_api_file = ApiFile(
            api_file_name='endpoint_file',
            host='127.0.0.1',
            imports=[],
            apis=[],
            variables=[],
            port=8000,
        )
        json_api_file = json.loads(json_api)
        api_file = self.fileProvider.cast(json_api=json_api_file)
        
        assert result_api_file == api_file

    def test_get_api_file_lines(self):
        api = Api(
            api_name='app',
            main_api=True,
            endpoints=[],
            api_file_name='endpoint_file',
            )
        api_file = ApiFile(
            api_file_name='endpoint_file',
            host='127.0.0.1',
            imports=[],
            apis=[api],
            variables=[],
            port=8000,
        )
        result_api_file_lines = [
            '\n',
            'subapp = importlib.import_module("api_name", "api_file_name")',
            'api_file_name.include_router(subapp.router)']

        api_file_lines = self.fileProvider.get_api_file_lines('api_name', "api_file_name")

        assert api_file_lines == result_api_file_lines

    def test_write_file_writelines(self):
        file_path = os.path.dirname(__file__)
        file_name = 'data/test_data_write.txt'
        lines = [
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
            "Aliquam tincidunt mauris eu risus.",
            "Vestibulum auctor dapibus neque."]
        with patch('builtins.open', unittest.mock.mock_open()) as mock:
            data_reader = FileProvider('','')
            data_reader.write_file(
                lines=lines,
                mode='w')

        #assert os.path.exists(file_path)
        mock.assert_called_once_with('{}/apps/source.json'.format(script_dir), 'w')
        handle = mock()
        handle.writelines.assert_called()
