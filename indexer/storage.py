from os import mkdir
from os.path import join, isdir
from pathlib import Path
import time
import json
import glob

from indexer import api

STORAGE_PATH = join(Path.home(), '.pastebrowser')
METADATA_PATH = join(STORAGE_PATH, 'metadata')
SAVED_PATH = join(STORAGE_PATH, 'saved')

class BasicStorage(object):
    @staticmethod
    def setup():
        if not isdir(STORAGE_PATH):
            mkdir(STORAGE_PATH)
        if not isdir(METADATA_PATH):
            mkdir(METADATA_PATH)
        if not isdir(SAVED_PATH):
            mkdir(SAVED_PATH)

    @staticmethod
    def store(note, truncated=True, name=None):
        if not name:
            name = note['key']
        BasicStorage.store_metadata(note)
        note_path = join('{}'.format(STORAGE_PATH), '{}.json'.format(name))
        with open(note_path, 'w+') as fp:
            if int(note['size']) > 250 and truncated:
                fp.write(api.PastebinAPI.get_raw(note['key'])[:249])
            else:
                fp.write(api.PastebinAPI.get_raw(note['key']))
    @staticmethod
    def load_note(syntax, key):
        note_path = join('{}'.format(STORAGE_PATH), '{}.json'.format(key))
        with open(note_path, 'r') as fp:
            return fp.read()
        return None

    @staticmethod
    def store_metadata(note):
        metadata_path = join(METADATA_PATH, '{}.json'.format(note['key']))
        with open(metadata_path, 'w+') as metadata_fp:
            metadata = note
            del note['scrape_url']
            metadata['date'] = time.ctime(int(note['date']))
            metadata['expire'] = time.ctime(int(note['expire']))
            json.dump(metadata, metadata_fp)

    @staticmethod
    def load_metadata(key):
        metadata_path = join(METADATA_PATH, '{}.json'.format(key))
        with open(metadata_path, 'r') as metadata_fp:
            return json.load(metadata_fp)
        return None

    @staticmethod
    def save_key(key, name):
        file_path = join(SAVED_PATH, '{}'.format(name))
        with open(file_path, 'w+') as fp:
            fp.write(api.PastebinAPI.get_raw(key))

    @staticmethod
    def get_files():
        return glob.glob(join(STORAGE_PATH, '*.json'))