from indexer import api, storage
import concurrent.futures
import sys


class Indexer(object):
    def __init__(self):
        self.tracker = 0
        storage.BasicStorage.setup()

    def index(self, callback):
        notes = list(api.PastebinAPI.get_recents())
        sys.stdout.write('refreshing...')
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(notes)) as executor:
            executor.map(storage.BasicStorage.store, notes)
        sys.stdout.write('...done!\n')

    def forward(self):
        self.tracker += 1

    def back(self):
        self.tracker -= 1
