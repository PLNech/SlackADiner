import os
import slack
from diner import get_meal

client = slack.WebClient(
    token=os.environ["SLACK_API_TOKEN"]
)


def format_text(fr, en, number):
    return """
Hi everyone :sir:

Today you can eat *{en}* (_{fr}_ :cow:)

There is {number} left, hurry!
""".format(
        fr=fr, en=en, number=number
    )


def send():
    response = client.chat_postMessage(
        channel="#test",
        text=format_text(*get_meal()),
        attachments=[
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
        ],
    )
    print("message sent!")
    return response


if __name__ == "__main__":
    send()
