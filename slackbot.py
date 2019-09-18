#! /usr/bin/env python
import os
from datetime import date

import slack

from diner import get_dishes
from menu import Menu


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
        text, attachments = SlackBot.make_message(get_dishes())
        self.response = self.client.chat_postMessage(
            channel=os.environ['SLACK_CHANNEL'],
            # channel="#office-paris-lunch",
            text=text,
            attachments=attachments,
        )
        print("message sent!")
        return self.response

    def update_diner(self, channel_id, ts):
        # TODO: Test scheduling an update
        text, attachments = SlackBot.make_message(*get_dishes())
        self.client.chat_update(
            channel=channel_id,
            ts=ts,
            text=text,
            attachments=attachments,
        )

    @staticmethod
    def format_dish(fr, en, quantity):
        number_str = str(quantity) if quantity > 2 else "*only one*"
        return """• *{en}* (_{fr}_ :cow:)
        There is {number} left, hurry!""".format(fr=fr, en=en, number=number_str)

    @staticmethod
    def make_message(menu: Menu):
        text = "Hi everyone :sir:\n"

        if menu.has_food:
            text += "Today you can eat:\n\n"
            if len(menu.meals):
                text += SlackBot.format_one_or_some(menu.meals, "meal")
                text += "\n".join([SlackBot.format_dish(*m) for m in menu.meals])
            if len(menu.deserts):
                text += SlackBot.format_one_or_some(menu.deserts, "desert")
                text += "\n".join([SlackBot.format_dish(*m) for m in menu.deserts])

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
            text += "Currently no Prêt À Diner is available :okay_sad:"
            attachments = None
        return text, attachments

    @staticmethod
    def format_one_or_some(dishes, name):
        return ("Some %ss" % name if len(dishes) > 1 else "A %s" % name) + ":"

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
