#! /usr/bin/env python

import os

import slack

from diner import get_meals

client = slack.WebClient(
    token=os.environ["SLACK_API_TOKEN"]
)


def format_meal(fr, en, number):
    number_str = str(number) if number > 2 else "*only one*"
    return """• *{en}* (_{fr}_ :cow:)
There is {number} left, hurry!""".format(fr=fr, en=en, number=number_str)


def make_message(meals):
    text = "Hi everyone :sir:\n"

    if len(meals):
        text += "Today you can eat:\n\n"
        text += "\n".join([format_meal(*m) for m in meals])
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


def send():
    text, attachments = make_message(get_meals())
    response = client.chat_postMessage(
        channel=os.environ['SLACK_CHANNEL'],
        # channel="#office-paris-lunch",
        text=text,
        attachments=attachments,
    )
    print("message sent!")
    return response


def update(channel_id, ts):
    text, attachments = make_message(*get_meal())
    client.chat_update(
        channel=channel_id,
        ts=ts,
        text=text,
        attachments=attachments,
    )


if __name__ == "__main__":
    response = send()
    print(response)  # this contains channel & ts, used for updating
