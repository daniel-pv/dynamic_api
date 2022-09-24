import sys
from watchdog.events import FileSystemEventHandler
from provider.fileprovider import FileProvider
from provider.sqliteProvider import SQLIteProvider
from endpointmanager import EndpointManager
folder_path_destiny = ''
file_name_destiny = ''
folder_path_origin = 'source'
file_name_origin = 'source.json'
data_base_origin = 'sqlite.db'
# data_base_origin = 'sqlite.db'


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        data_base_origin = sys.argv[1]
        print('Data base:{}'.format(sys.argv[1]))
    if len(sys.argv) > 2:
        folder_path_destiny = sys.argv[2]
        folder_path_origin = sys.argv[2]
        print('Folder path:{}'.format(sys.argv[2]))
    if len(sys.argv) > 3:
        file_name_origin = sys.argv[3]
        print('File name:{}'.format(sys.argv[3]))

    destinyProvider = FileProvider(file_name_destiny, folder_path_destiny)
    originProvider = SQLIteProvider(db_name=data_base_origin, db_file=data_base_origin)
    endpoint_manag = EndpointManager(destinyProvider, originProvider)
    endpoint_manag.run()

    print('End')
