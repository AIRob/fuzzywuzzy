# -*- coding: utf8 -*-

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fuzzywuzzy import utils
from fuzzywuzzy.string_processing import StringProcessor

import itertools
import unittest
import re

class StringProcessingTest(unittest.TestCase):
    def test_replace_non_lettters_non_numbers_with_whitespace(self):
        strings = [u"new york mets - atlanta braves", u"Cães danados", u"New York //// Mets $$$", u"Ça va?"]
        for string in strings:
            proc_string = StringProcessor.replace_non_lettters_non_numbers_with_whitespace(string)
            regex = re.compile(r"(?ui)[\W]+")
            for expr in regex.finditer(proc_string):
                self.assertEquals(expr.group(), " ")

class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.s1 = "new york mets"
        self.s1a = "new york mets"
        self.s2 = "new YORK mets"
        self.s3 = "the wonderful new york mets"
        self.s4 = "new york mets vs atlanta braves"
        self.s5 = "atlanta braves vs new york mets"
        self.s6 = "new york mets - atlanta braves"
        self.mixed_strings = [
            u"Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
            u"C'est la vie",
            u"Ça va?",
            u"Cães danados",
            u"\xacCamarões assados",
            u"a\xac\u1234\u20ac\U00008000",
            u"\u00C1"
        ]

    def tearDown(self):
        pass

    def test_asciidammit(self):
        for s in self.mixed_strings:
            utils.asciidammit(s)

    def test_asciionly(self):
        for s in self.mixed_strings:
            # ascii only only runs on strings
            s = utils.asciidammit(s)
            utils.asciionly(s)

    def test_fullProcess(self):
        for s in self.mixed_strings:
            utils.full_process(s)

    def test_fullProcessForceAscii(self):
        for s in self.mixed_strings:
            utils.full_process(s, force_ascii=True)

class RatioTest(unittest.TestCase):

    def setUp(self):
        self.s1 = "new york mets"
        self.s1a = "new york mets"
        self.s2 = "new YORK mets"
        self.s3 = "the wonderful new york mets"
        self.s4 = "new york mets vs atlanta braves"
        self.s5 = "atlanta braves vs new york mets"
        self.s6 = "new york mets - atlanta braves"

        self.cirque_strings = [
            "cirque du soleil - zarkana - las vegas",
            "cirque du soleil ",
            "cirque du soleil las vegas",
            "zarkana las vegas",
            "las vegas cirque du soleil at the bellagio",
            "zarakana - cirque du soleil - bellagio"
        ]

        self.baseball_strings = [
            "new york mets vs chicago cubs",
            "chicago cubs vs chicago white sox",
            "philladelphia phillies vs atlanta braves",
            "braves vs mets",
        ]

    def tearDown(self):
        pass

    def testEqual(self):
        self.assertEqual(fuzz.ratio(self.s1, self.s1a),100)

    def testCaseInsensitive(self):
        self.assertNotEqual(fuzz.ratio(self.s1, self.s2),100)
        self.assertEqual(fuzz.ratio(utils.full_process(self.s1), utils.full_process(self.s2)),100)

    def testPartialRatio(self):
        self.assertEqual(fuzz.partial_ratio(self.s1, self.s3),100)

    def testTokenSortRatio(self):
        self.assertEqual(fuzz.token_sort_ratio(self.s1, self.s1a),100)

    def testPartialTokenSortRatio(self):
        self.assertEqual(fuzz.partial_token_sort_ratio(self.s1, self.s1a),100)
        self.assertEqual(fuzz.partial_token_sort_ratio(self.s4, self.s5),100)

    def testTokenSetRatio(self):
        self.assertEqual(fuzz.token_set_ratio(self.s4, self.s5),100)

    def testPartialTokenSetRatio(self):
        self.assertEqual(fuzz.token_set_ratio(self.s4, self.s5),100)

    def testQuickRatioEqual(self):
        self.assertEqual(fuzz.QRatio(self.s1, self.s1a), 100)

    def testQuickRatioCaseInsensitive(self):
        self.assertEqual(fuzz.QRatio(self.s1, self.s2), 100)

    def testQuickRatioNotEqual(self):
        self.assertNotEqual(fuzz.QRatio(self.s1, self.s3), 100)

    def testWRatioEqual(self):
        self.assertEqual(fuzz.WRatio(self.s1, self.s1a), 100)

    def testWRatioCaseInsensitive(self):
        self.assertEqual(fuzz.WRatio(self.s1, self.s2), 100)

    def testWRatioPartialMatch(self):
        # a partial match is scaled by .9
        self.assertEqual(fuzz.WRatio(self.s1, self.s3), 90)

    def testWRatioMisorderedMatch(self):
        # misordered full matches are scaled by .95
        self.assertEqual(fuzz.WRatio(self.s4, self.s5), 95)

    def testWRatioUnicode(self):
        self.assertEqual(fuzz.WRatio(unicode(self.s1), unicode(self.s1a)), 100)

    def testQRatioUnicode(self):
        self.assertEqual(fuzz.WRatio(unicode(self.s1), unicode(self.s1a)), 100)

    def testIssueSeven(self):
        s1 = "HSINCHUANG"
        s2 = "SINJHUAN"
        s3 = "LSINJHUANG DISTRIC"
        s4 = "SINJHUANG DISTRICT"

        self.assertTrue(fuzz.partial_ratio(s1, s2) > 75)
        self.assertTrue(fuzz.partial_ratio(s1, s3) > 75)
        self.assertTrue(fuzz.partial_ratio(s1, s4) > 75)

    def testWRatioUnicodeString(self):
        s1 = u"\u00C1"
        s2 = u"ABCD"
        score = fuzz.WRatio(s1, s2)
        self.assertEqual(0, score)

        # Cyrillic.
        s1 = u"\u043f\u0441\u0438\u0445\u043e\u043b\u043e\u0433"
        s2 = u"\u043f\u0441\u0438\u0445\u043e\u0442\u0435\u0440\u0430\u043f\u0435\u0432\u0442"
        score = fuzz.WRatio(s1, s2)
        self.assertNotEqual(0, score)

        # Chinese.
        s1 = u"\u6211\u4e86\u89e3\u6570\u5b66"
        s2 = u"\u6211\u5b66\u6570\u5b66"
        score = fuzz.WRatio(s1, s2)
        self.assertNotEqual(0, score)

    def testQRatioUnicodeString(self):
        s1 = u"\u00C1"
        s2 = u"ABCD"
        score = fuzz.QRatio(s1, s2)
        self.assertEqual(0, score)

        # Cyrillic.
        s1 = u"\u043f\u0441\u0438\u0445\u043e\u043b\u043e\u0433"
        s2 = u"\u043f\u0441\u0438\u0445\u043e\u0442\u0435\u0440\u0430\u043f\u0435\u0432\u0442"
        score = fuzz.QRatio(s1, s2)
        self.assertNotEqual(0, score)

        # Chinese.
        s1 = u"\u6211\u4e86\u89e3\u6570\u5b66"
        s2 = u"\u6211\u5b66\u6570\u5b66"
        score = fuzz.QRatio(s1, s2)
        self.assertNotEqual(0, score)

    def testQratioForceAscii(self):
        s1 = u"ABCD\u00C1"
        s2 = u"ABCD"

        score = fuzz.QRatio(s1, s2, force_ascii=True)
        self.assertEqual(score, 100)

        score = fuzz.QRatio(s1, s2, force_ascii=False)
        self.assertLess(score, 100)

    def testQRatioForceAscii(self):
        s1 = u"ABCD\u00C1"
        s2 = u"ABCD"

        score = fuzz.WRatio(s1, s2, force_ascii=True)
        self.assertEqual(score, 100)

        score = fuzz.WRatio(s1, s2, force_ascii=False)
        self.assertLess(score, 100)

    def testTokenSetForceAscii(self):
        s1 = u"ABCD\u00C1 HELP\u00C1"
        s2 = u"ABCD HELP"

        score = fuzz._token_set(s1, s2, force_ascii=True)
        self.assertEqual(score, 100)

        score = fuzz._token_set(s1, s2, force_ascii=False)
        self.assertLess(score, 100)

    def testTokenSortForceAscii(self):
        s1 = u"ABCD\u00C1 HELP\u00C1"
        s2 = u"ABCD HELP"

        score = fuzz._token_sort(s1, s2, force_ascii=True)
        self.assertEqual(score, 100)

        score = fuzz._token_sort(s1, s2, force_ascii=False)
        self.assertLess(score, 100)



    # test processing methods
    def testGetBestChoice1(self):
        query = "new york mets at atlanta braves"
        best = process.extractOne(query, self.baseball_strings)
        self.assertEqual(best[0], "braves vs mets")

    def testGetBestChoice2(self):
        query = "philadelphia phillies at atlanta braves"
        best = process.extractOne(query, self.baseball_strings)
        self.assertEqual(best[0], self.baseball_strings[2])

    def testGetBestChoice3(self):
        query = "atlanta braves at philadelphia phillies"
        best = process.extractOne(query, self.baseball_strings)
        self.assertEqual(best[0], self.baseball_strings[2])

    def testGetBestChoice4(self):
        query = "chicago cubs vs new york mets"
        best = process.extractOne(query, self.baseball_strings)
        self.assertEqual(best[0], self.baseball_strings[0])

class ProcessTest(unittest.TestCase):

    def setUp(self):
        self.s1 = "new york mets"
        self.s1a = "new york mets"
        self.s2 = "new YORK mets"
        self.s3 = "the wonderful new york mets"
        self.s4 = "new york mets vs atlanta braves"
        self.s5 = "atlanta braves vs new york mets"
        self.s6 = "new york mets - atlanta braves"

        self.cirque_strings = [
            "cirque du soleil - zarkana - las vegas",
            "cirque du soleil ",
            "cirque du soleil las vegas",
            "zarkana las vegas",
            "las vegas cirque du soleil at the bellagio",
            "zarakana - cirque du soleil - bellagio"
        ]

        self.baseball_strings = [
            "new york mets vs chicago cubs",
            "chicago cubs vs chicago white sox",
            "philladelphia phillies vs atlanta braves",
            "braves vs mets",
        ]

    def testWithProcessor(self):
        events = [
            ["chicago cubs vs new york mets", "CitiField", "2011-05-11", "8pm"],
            ["new york yankees vs boston red sox", "Fenway Park", "2011-05-11", "8pm"],
            ["atlanta braves vs pittsburgh pirates", "PNC Park", "2011-05-11", "8pm"],
        ]
        query = "new york mets vs chicago cubs"
        processor = lambda event: event[0]

        best = process.extractOne(query, events, processor=processor)
        self.assertEqual(best[0], events[0])

    def testWithScorer(self):
        choices = [
            "new york mets vs chicago cubs",
            "chicago cubs at new york mets",
            "atlanta braves vs pittsbugh pirates",
            "new york yankees vs boston red sox"
        ]

        # in this hypothetical example we care about ordering, so we use quick ratio
        query = "new york mets at chicago cubs"
        scorer = fuzz.QRatio

        # first, as an example, the normal way would select the "more 'complete' match of choices[1]"

        best = process.extractOne(query, choices)
        self.assertEqual(best[0], choices[1])

        # now, use the custom scorer

        best = process.extractOne(query, choices, scorer=scorer)
        self.assertEqual(best[0], choices[0])

    def testWithCutoff(self):
        choices = [
            "new york mets vs chicago cubs",
            "chicago cubs at new york mets",
            "atlanta braves vs pittsbugh pirates",
            "new york yankees vs boston red sox"
        ]

        query = "los angeles dodgers vs san francisco giants"

        # in this situation, this is an event that does not exist in the list
        # we don't want to randomly match to something, so we use a reasonable cutoff

        best = process.extractOne(query, choices, score_cutoff=50)
        self.assertTrue(best is None)
        #self.assertIsNone(best) # unittest.TestCase did not have assertIsNone until Python 2.7

        # however if we had no cutoff, something would get returned

        #best = process.extractOne(query, choices)
        #self.assertIsNotNone(best)

    def testEmptyStrings(self):
        choices = [
            "",
            "new york mets vs chicago cubs",
            "new york yankees vs boston red sox",
            "",
            ""
        ]

        query = "new york mets at chicago cubs"

        best = process.extractOne(query, choices)
        self.assertEqual(best[0], choices[1])

    def testNullStrings(self):
        choices = [
            None,
            "new york mets vs chicago cubs",
            "new york yankees vs boston red sox",
            None,
            None
        ]

        query = "new york mets at chicago cubs"

        best = process.extractOne(query, choices)
        self.assertEqual(best[0], choices[1])


if __name__ == '__main__':
    unittest.main()         # run all tests
