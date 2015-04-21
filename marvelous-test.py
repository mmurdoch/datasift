from marvelous import CharacterRetriever
from marvelous import InteractionReceiver
from marvelous import ResponseError
from marvelous import TimeoutError
import requests.exceptions
import unittest


class CharacterRetrieverTest(unittest.TestCase):
    RETRIEVER = CharacterRetriever('public_key', 'private_key')

    def test_is_character_file(self):
        self.assertTrue(self.RETRIEVER._is_character_file('characters-20-38'))

    def test_is_not_character_file(self):
        self.assertFalse(self.RETRIEVER._is_character_file('marvelous.py'))

    def test_timeout_returns_no_characters(self):
        def timeout_thrower(uri, **kwargs):
            raise requests.exceptions.Timeout

        try:
            self.RETRIEVER._get_characters(timeout_thrower, 0)
            self.fail()
        except TimeoutError:
            # Success
            pass

    def test_bad_status_code_returns_no_characters(self):
        def bad_status_code_returner(uri, **kwargs):
            class BadResponse(object):
                @property
                def status_code(self):
                    return 409

                @property
                def reason(self):
                    return 'Invalid or unrecognized parameter'
            return BadResponse()

        try:
            self.RETRIEVER._get_characters(bad_status_code_returner, 0)
            self.fail()
        except ResponseError:
            # Success
            pass


class InteractionReceiverTest(unittest.TestCase):
    def test_get_csdl(self):
        receiver = InteractionReceiver('username', 'api_key')
        self.assertEquals('interaction.type == "tumblr" AND ' +
               'language.tag == "en" AND ' +
               '(' +
               'interaction.content contains_any "Apeman,Human" OR ' +
               'interaction.hashtags contains_any "Apeman,Human"' +
               ')', receiver.get_csdl('Apeman,Human'))


if __name__ == '__main__':
    unittest.main()
