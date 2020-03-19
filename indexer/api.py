import requests
import json


class PastebinAPI(object):
    @staticmethod
    def get_raw(key):
        """
        Gets the raw text of a note
        :param key: 'Key' or ID of the note
        :return: the raw text as a string
        """
        r = requests.get('https://pastebin.com/raw/{}'.format(key))
        return r.text

    @staticmethod
    def get_recents():
        """
        Iteratively returns each note in the most recent 50 posted notes
        :return:
        """
        r = requests.get('https://scrape.pastebin.com/api_scraping.php')
        recent_notes = json.loads(r.text)
        for note in recent_notes:
            yield note
