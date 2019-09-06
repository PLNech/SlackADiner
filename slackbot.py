import os
import slack
from diner import get_meal

client = slack.WebClient(
    token=os.environ["SLACK_API_TOKEN"]
)


def make_message(fr, en, number):
    text = """
Hi everyone :sir:

Today you can eat *{en}* (_{fr}_ :cow:)

There is {number} left, hurry!
""".format(
        fr=fr, en=en, number=number
    )

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

    return text, attachments


def send():
    text, attachments = make_message(*get_meal())
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
    response = client.chat_update(
        channel=channel_id,
        ts=ts,
        text=text,
        attachments=attachments,
    )

if __name__ == "__main__":
    response = send()
    print(response) # this contains channel & ts, used for updating
