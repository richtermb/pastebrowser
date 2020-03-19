from indexer import api, storage


class Indexer(object):
    def __init__(self):
        self.tracker = 0
        storage.BasicStorage.setup()

    def index(self, callback):
        for note in api.PastebinAPI.get_recents():
            storage.BasicStorage.store(note)
            callback()

    def forward(self):
        self.tracker += 1

    def back(self):
        self.tracker -= 1
