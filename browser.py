from indexer import indexer
import googletrans
import random
import requests
import os

PROMPT = """Pastebrowser V1.0
1) See next note
2) Key search
3) Refresh"""

NOTE_HELP = """Note Inspector
t) Translate
"""

if __name__ == '__main__':
    print(PROMPT)
    idxr = indexer.Indexer()
    notes = indexer.storage.BasicStorage.get_files()
    random.shuffle(notes)

    while True:
        command = input()
        if len(command) == 0:
            # just pressing enter key will display next note
            command = '1'
        if command == '1':
            idxr.forward()
            with open(notes[idxr.tracker], 'r') as fp:
                print('{}\n'.format(fp.read()))
            print('-' * 20)
        elif command == '`':
            idxr.back()
            with open(notes[idxr.tracker], 'r') as fp:
                print('{}\n'.format(fp.read()))
        elif command == '2':
            print('Key: ')
            key = input()
            print(indexer.api.PastebinAPI.get_raw(key))
        elif command == '3':
            idxr.index()
            notes = indexer.storage.BasicStorage.get_files()
            random.shuffle(notes)
        elif command == 't':
            with open(notes[idxr.tracker], 'r') as fp:
                translator = googletrans.Translator()
                xlated = translator.translate(fp.read())
                print(xlated.text)
        elif command == 'o':
            derived_key = notes[idxr.tracker].split('/')[-1].replace('.json', '')
            metadata = indexer.storage.BasicStorage.load_metadata(derived_key)
            print(metadata)
            print(indexer.api.PastebinAPI.get_raw(derived_key))
        elif command == 'l':
            print('length:{}'.format(len(notes)))
            print('max disk space: {} bytes'.format(250 * len(notes)))
        elif command == 'g':
            r = requests.get()
        elif command == 'd':
            os.remove(notes[idxr.tracker])
            print('removed.')
            notes = indexer.storage.BasicStorage.get_files()
            random.shuffle(notes)
        elif command[0] == '>':
            derived_key = notes[idxr.tracker].split('/')[-1].replace('.json', '')
            indexer.storage.BasicStorage.save_key(derived_key, command.split('>')[1])
            print('saved paste.')
        else:
            print('invalid command...')