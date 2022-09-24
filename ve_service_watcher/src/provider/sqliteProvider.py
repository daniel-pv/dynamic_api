import sqlite3
from sqlite3 import Error
import logging
from entities.endpoint import ApiFile, Api, EndPoint
from provider.originAdapter import OriginAdapter


class SQLIteProvider(OriginAdapter):
    def __init__(self, db_name='', db_file=''):
        super().__init__(source_path=db_file, source_name=db_name)
        self._connection = None

    @property
    def connection(self):
        if not self._connection:
            return self.create_connection(self.source_name)

    @connection.setter
    def connection(self, value):
        self._connection = value

    def read(self) -> ApiFile:
        api_file = None
        try:
            data = self.connection.execute("select * from ApiFile")
            api_file = self.get_api_file_data(data)
        except Exception:
            logging.error(
                'It was not possible to read data from database[Name{}]'
                .format(self.source_name))
        finally:
            self.connection.close()

        return api_file

# region Helpers
    def get_api_file_data(self, data_set):
        api_file = None
        print(type(data_set))
        for index, data in enumerate(data_set):
            id = data[0]
            name = data[1]
            port = data[2]
            host = data[3]
            api_file = ApiFile(
                api_file_name=name,
                port=port,
                host=host,
                apis=self.get_api_data(id=id, api_file_name=name),
                imports=self.get_imports(id=id),
                variables=self.get_variables(id=id),
            )
            if index < 1:
                break

        return api_file

    def get_api_data(self, id: int, api_file_name):
        apis = []
        data_set = self.connection.execute(
            'select * from Api where api_file_id={}'
            .format(id))

        for data in data_set:
            id = data[0]
            name = data[1]
            main = True if data[2] == 1 else False
            endpoints = self.get_endpoint_data(id=id, api_name=name)

            api = Api(
                api_name=name,
                main_api=main,
                endpoints=endpoints,
                api_file_name=api_file_name,
            )
            apis.append(api)

        return apis

    def get_endpoint_data(self, id: int, api_name):
        endpoints = []
        data_set = self.connection.execute(
            'select * from EndPoint where api_id={}'
            .format(id))

        for data in data_set:
            id = data[0]
            name = data[1]
            method = data[2]
            route = data[3]
            params = data[4]
            payload = data[5]

            endpoint = EndPoint(
                name=name,
                method=method,
                route=route,
                params=params if params else '',
                payload=payload if payload else '',
                api_name=api_name,
            )
            endpoints.append(endpoint)

        return endpoints

    def get_imports(self, id: int):
        imports = []
        data_set = self.connection.execute(
            'select * from Import where api_file_id={}'
            .format(id))

        for data in data_set:
            imports.append(data[1])

        return imports

    def get_variables(self, id: int):
        variables = []
        data_set = self.connection.execute(
            'select * from Variable where api_file_id={}'
            .format(id))

        for data in data_set:
            variables.append(data[1])

        return variables

    def create_connection(self, db_file):
        conection = None
        try:
            conection = sqlite3.connect(db_file)
            logging.info(sqlite3.version)
        except Error as e:
            logging.error(e)

        return conection
# endregion
