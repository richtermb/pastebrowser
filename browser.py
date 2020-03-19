from indexer import indexer
import googletrans
import random


def refresh():
    print('stored note')

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
        if command == '1':
            idxr.forward()
            with open(notes[idxr.tracker], 'r') as fp:
                print('{}\n'.format(fp.read()))
        if command == '`':
            idxr.back()
            with open(notes[idxr.tracker], 'r') as fp:
                print('{}\n'.format(fp.read()))
        if command == '2':
            print('Key: ')
            key = input()
            print(indexer.api.PastebinAPI.get_raw(key))
        if command == '3':
            idxr.index(refresh)
            notes = indexer.storage.BasicStorage.get_files()
        if command == 't':
            with open(notes[idxr.tracker], 'r') as fp:
                translator = googletrans.Translator()
                xlated = translator.translate(fp.read())
                print(xlated.text)
        if command == 'o':
            derived_key = notes[idxr.tracker].split('/')[-1].replace('.json', '')
            metadata = indexer.storage.BasicStorage.load_metadata(derived_key)
            print(indexer.api.PastebinAPI.get_raw(derived_key))
        if command == 'l':
            print('length:{}'.format(len(notes)))
