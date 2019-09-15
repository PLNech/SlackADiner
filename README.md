# SlackADiner

A SlackBot to let you know what is up for pret-a-diner tonight!

![screenshot of the bot in action for the first time](screenshot.png)

## Requirements:

- having prêt-à-diner at your company's canteen
- setting environment variables for credentials and parameters:
  - Sogeres (sohappy@work account) credentials (`SOHAPPY_USERNAME` and `SOHAPPY_PASSWORD`)
  - SlackBot API token (`SLACK_API_TOKEN`)
  - Slack channel to post into (`SLACK_CHANNEL`)
- Python3.6+
- set up Heroku scheduling for when the menu will be available (around 2.30, 3PM should be safe)

## Plans

- slash-command to see regular lunch menu
- send the regular lunch menu
- slash-command to ask for pret-a-diner menu
