#! /usr/bin/env python
import os
from datetime import date, datetime

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
    def format_dish(fr: str, en: str, quantity: int = None) -> dict:
        """Formats the dish as an attachment' field.

        :param fr: Its french name.
        :param en: Its english name.
        :param quantity: When specified, how many dishes are available.
        """

        if quantity is not None:
            plural = quantity >= 2
            fr = fr + """
        There {verb} {number} left, hurry!""".format(verb="are" if plural else "is",
                                                     number=quantity if plural else "*only one*")

        return {
            "title": ":flag-us: %s" % en,
            "value": ":flag-fr: %s" % fr,
            "short": False
        }

    @staticmethod
    def make_message(menu: Menu):
        colors = {"starter": "#1B9135", "meal": "#186876", "side": "#C07024", "dessert": "#C03324"}
        is_diner = type(menu) is Diner
        title = "_Prêt à dîner_" if is_diner else "Lunch"
        text = "Hi everyone, here's today's %s menu :sir:\n" % title

        if menu.has_food:
            attachments = []
            # Let's show meals first, then deserts and starters, ignoring sides
            for composante, name in [(menu.plats, "meal"), (menu.desserts, "dessert"), (menu.entrees, "starter")]:
                if len(composante):
                    dishes = [SlackBot.format_dish(fr, en, quantity) for fr, en, quantity in composante]
                    dishes_title = SlackBot.format_one_or_some(composante, name)
                    dishes_string = dishes_title + str(composante)

                    attachments.append({
                        "fallback": dishes_string,
                        "color": colors[name],
                        "title": dishes_title,
                        "fields": dishes,
                        "mrkdwn_in": [
                            "fields"
                        ]
                    })
            if is_diner:
                attachments.append({  # Add the CTA
                    "fallback": "Grab the food at https://55-amsterdam.sohappy.work/index.cfm?e=zr&id=1968",
                    "actions": [
                        {
                            "type": "button",
                            "text": "Grab the food 😋",
                            "url": "https://55-amsterdam.sohappy.work/index.cfm?e=zr&id=1968",
                        }
                    ],
                })
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
        response = bot.send_lunch() if datetime.now().hour < 12 else bot.send_diner()
        print(response)  # this contains channel & ts, used for updating
