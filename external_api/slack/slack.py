import json
from datetime import datetime as dt

import requests

from slackclient import SlackClient

HEADERS = {'content-type': 'application/json'}


class Slack:
    """Interactions with slack""" 
    CONFIG_TEMPLATE = "conf/%s.json"

    def __init__(self, verification_token, bot_token):
        self.verification_token = verification_token
        self.client = SlackClient(bot_token)

    def send_teams_form(self, user_id, request_token):

        # Verify token
        self._verify_slack_token(user_id, request_token)

        # Open and load the teams json file
        with open(self.CONFIG_TEMPLATE % 'Teams') as f:
            form = json.load(f)

        attachments_json = [form]

        # Submit the list of available teams
        self.client.api_call(
            "chat.postMessage",
            channel="#agatha-testes",
            text="Hi, I'll help you",
            attachments=attachments_json
        )
        
        return "", 200
    
    def send_ticket_form(self, trigger, team, response_url):
        # Open and load the form file
        with open(self.CONFIG_TEMPLATE % (team)) as f:
            form = json.load(f)

        form["state"] = json.dumps(form["state"])

        body = {
            "replace_original": "true",
            "text": "Ticket for " + team + " team!"
        }
        # Close the first user interaction
        requests.post(response_url, data=json.dumps(body),
                      headers=HEADERS)

        # Open the ticket dialog with the user
        self.client.api_call(
            "dialog.open",
            trigger_id=trigger,
            dialog=form
        )

        return ""

    def _verify_slack_token(self, user, request_token):
        # Verify slack token
        if(request_token != self.verification_token):
            error_msg = "Request contains invalid Slack verification token"
            self.client.api_call(
                "chat.postEphemeral",
                user=user,
                channel="#agatha-testes",
                text=error_msg
            )
            raise Exception(error_msg)
        return ""

    def new_ticket_message_public(self, user, description, team):
        # The message will be sent as soon as the function is called
        ts = dt.now()
        # Send a message that may be visible to everyone in the group
        self.client.api_call(
            "chat.postMessage",
            channel="#agatha-testes",
            text="Ticket created with success! \n User: " + user +
            "\n Team: " + team + "\n Issue: " + description,
            ts=ts
        )
        return ""

    def new_ticket_message_private(self):
        # The message will be sent as soon as the function is called
        ts = dt.now()
        # Send a message that cannot be visible to everyone in the group
        self.client.api_call(
            "chat.postMessage",
            channel="#agatha-testes",
            text="New ticket created with success!",
            ts=ts
        )

        return ""

    def retrieve_requester(self):
        requester = self.email

        return requester
