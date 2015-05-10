from marvelous import CharacterRetriever
from marvelous import InteractionStreamProcessor
from marvelous import CharacterSentimentStatistics
from marvelous import ResponseError
from marvelous import TimeoutError
import requests.exceptions
import unittest


class CharacterRetrieverTest(unittest.TestCase):
    RETRIEVER = CharacterRetriever('public_key', 'private_key')

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


class InteractionStreamProcessorTest(unittest.TestCase):
    PROCESSOR = InteractionStreamProcessor('username', 'api_key', None)

    def test_escape_for_contains_any(self):
        self.assertEquals(r'\\ \" \,',
            self.PROCESSOR._escape_for_contains_any(r'\ " ,'))

    def test_get_csdl(self):
        self.assertEquals(
            'tag "Apeman" { interaction.content contains "Apeman" OR ' +
            'interaction.hashtags contains "Apeman" } ' +
            'tag "Human" { interaction.content contains "Human" OR ' +
            'interaction.hashtags contains "Human" } ' +
            'return { interaction.type == "tumblr" AND ' +
            'language.tag == "en" AND ' +
            'interaction.content contains "marvel" AND ' +
            '(' +
            'interaction.content contains_any "Apeman,Human" OR ' +
            'interaction.hashtags contains_any "Apeman,Human"' +
            ') }', self.PROCESSOR._get_csdl(['Apeman','Human']))


class CharacterSentimentStatisticsTest(unittest.TestCase):
    def test_split_interaction(self):
        statistics = CharacterSentimentStatistics()

        statistics.add_sentiment([u'Name1', u'Name2'], 3)

        self.assertEquals([3], statistics._get_sentiments(u'Name1'))
        self.assertEquals([3], statistics._get_sentiments(u'Name2'))

    def test_add_two_interactions(self):
        statistics = CharacterSentimentStatistics()

        statistics.add_sentiment([u'Name1'], 2)
        statistics.add_sentiment([u'Name1'], 4)

        self.assertEquals([2,4], statistics._get_sentiments(u'Name1'))

    def test_get_mean_sentiment(self):
        statistics = CharacterSentimentStatistics()

        statistics.add_sentiment([u'N1'], 7)
        statistics.add_sentiment([u'N1'], 8)
        statistics.add_sentiment([u'N1'], 9)

        self.assertEquals(8, statistics._get_mean_sentiment(u'N1'))


if __name__ == '__main__':
    unittest.main()
