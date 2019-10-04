#! /usr/bin/env python
import os
from datetime import date

import slack

from menu import Diner, Menu
from scraper import get_diner, get_lunch


class SlackBot:

    def __init__(self):
        self._client = None
        self.response = None

    @property
    def client(self):
        if self._client is None:
            self._client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])
        return self._client

    def send_diner(self):
        text, attachments = SlackBot.make_message(get_diner())
        self.response = self.client.chat_postMessage(
            channel=os.environ['SLACK_CHANNEL'] if "SLACK_CHANNEL" in os.environ else "#test",
            text=text,
            attachments=attachments,
        )
        print("message sent!")
        return self.response

    def send_lunch(self):
        text, attachments = SlackBot.make_message(get_lunch())
        self.response = self.client.chat_postMessage(
            channel=os.environ['SLACK_CHANNEL'] if "SLACK_CHANNEL" in os.environ else "#test",
            text=text,
            attachments=attachments,
        )
        print("message sent!")
        return self.response

    def update_diner(self, channel_id, ts):
        # TODO: Test scheduling an update
        text, attachments = SlackBot.make_message(get_diner())
        self.client.chat_update(
            channel=channel_id,
            ts=ts,
            text=text,
            attachments=attachments,
        )

    @staticmethod
    def format_dish(fr, en, quantity=None):
        text = "• *{en}* (_{fr}_ :cow:)".format(fr=fr, en=en)
        if quantity is not None:
            text = text + """
        There is {number} left, hurry!""".format(number=str(quantity) if quantity > 2 else "*only one*")
        return text

    @staticmethod
    def make_message(menu: Menu):

        title = "_Prêt à dîner_" if menu is Diner else "Lunch"
        text = "Hi everyone, here's today's %s menu :sir:\n" % title

        if menu.has_food:
            for composante, name in [(menu.entrees, "starter"), (menu.plats, "meal"), (menu.garnitures, "side"),
                                     (menu.desserts, "dessert")]:
                print("handling composante %s: " % name, composante)
                print([len(i) for i in composante])
                if len(composante):
                    text += SlackBot.format_one_or_some(composante, name)
                    text += "\n".join([SlackBot.format_dish(*m) for m in composante])

            attachments = [
                {
                    "fallback": "Grab the food at https://55-amsterdam.sohappy.work/index.cfm?e=zr&id=1968",
                    "actions": [
                        {
                            "type": "button",
                            "text": "Grab the food 😋",
                            "url": "https://55-amsterdam.sohappy.work/index.cfm?e=zr&id=1968",
                        }
                    ],
                }
            ]

        else:
            text += "Currently no %s is available :okay_sad:" % title
            attachments = None
        return text, attachments

    @staticmethod
    def format_one_or_some(dishes, name):
        return "\n\n" + ("Some %ss" % name if len(dishes) > 1 else "A %s" % name) + ":\n"

    @staticmethod
    def is_canteen_day(day=date.today()):
        # TODO: Add bank holidays
        is_weekday = day.isoweekday() < 6

        if not is_weekday:
            print("No canteen on weekends.")
        return is_weekday


if __name__ == "__main__":
    bot = SlackBot()
    if SlackBot.is_canteen_day():
        response = bot.send_diner()
        print(response)  # this contains channel & ts, used for updating
