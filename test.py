import unittest
from datetime import date

from diner import with_missing_accents
from slackbot import SlackBot

mock_meal = ("Aubergines sautées", "sautéed eggplants", 10)


class SlackBotTestCase(unittest.TestCase):
    """ Tests for slackbot runner. """

    def setUp(self):
        self.bot = SlackBot()

    def test_is_canteen_day(self):
        saturday = date(2000, 1, 1)
        sunday = date(2000, 1, 2)
        monday = date(2000, 1, 3)
        tuesday = date(2000, 1, 4)
        wednesday = date(2000, 1, 5)
        thursday = date(2000, 1, 6)
        friday = date(2000, 1, 7)
        self.assertFalse(self.bot.is_canteen_day(saturday), "No canteen on saturdays")
        self.assertFalse(self.bot.is_canteen_day(sunday), "No canteen on sundays")
        self.assertTrue(self.bot.is_canteen_day(monday), "Canteen on mondays")
        self.assertTrue(self.bot.is_canteen_day(tuesday), "Canteen on tuesdays")
        self.assertTrue(self.bot.is_canteen_day(wednesday), "Canteen on wednesdays")
        self.assertTrue(self.bot.is_canteen_day(thursday), "Canteen on thursdays")
        self.assertTrue(self.bot.is_canteen_day(friday), "Canteen on fridays")

    def test_make_message(self):
        text, attachments = self.bot.make_message([])
        self.assertIsNone(attachments, "Empty meals should have no attachments")

        text, attachments = self.bot.make_message([mock_meal])
        self.assertIsNotNone(attachments, "Meals should have some attachments")

    def test_format_meal(self):
        (fr, en, q) = mock_meal
        text = self.bot.format_dish(fr, en, q)
        self.assertTrue(fr in text, "The text should contain the french dish")
        self.assertTrue(en in text, "The text should contain the english dish")
        self.assertTrue(str(q) in text, "The text should contain the quantity")


class DinerTestCase(unittest.TestCase):
    """ Tests for the diner scraper. """

    def test_with_missing_accents(self):
        self.assertEqual(with_missing_accents("porc saute"), "porc sauté")
        self.assertEqual(with_missing_accents("sauterelle"), "sauterelle")
        self.assertEqual(with_missing_accents("Roti braise"), "Roti braisé")
        self.assertEqual(with_missing_accents("Roti braise aux patates sautees"), "Roti braisé aux patates sautées")
