import json
from os import environ

from external_api.slack.slack import Slack
from flask import Flask, request

# Flask webserver for incoming traffic from Slack
app = Flask(__name__)

# Init Slack
slck = Slack(
    verification_token=environ.get("SLACK_TOKEN", "fe4fGSTvijxkKqiSXcriOJtR"),
    bot_token=environ.get(
        "BOT_TOKEN", "xoxb-1014442863923-1025839838629-eP5q7rD5nIZCfsi0WksknBwF")
)

# The Slack endpoint will send a ephemeral chat to start the dialog
@app.route("/slack/command", methods=["POST"])
def command():

    # Parse the request payload
    slash_json = request.form.to_dict()
    # Get the token and the user id to confirm that the request came from the slack
    request_token = slash_json["token"]
    user_id = slash_json["user_id"]

    # Start chat
    slck.send_teams_form(user_id, request_token)

    return "", 200

# The Slack endpoint will start the actions
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Send the list of available teams to the user
    if form_json["callback_id"] == "teams_options":

        trigger = form_json["trigger_id"]
        team = form_json["actions"][0]["selected_options"][0]["value"]
        response_url = form_json["response_url"]
        user_id = form_json["user"]["id"]

        slck.send_ticket_form(trigger, team, response_url)

    # After the user chooses the team, send the form of the chosen team
    elif form_json["callback_id"] == "ticket":

        user = form_json["user"]["name"]
        description = form_json["submission"]["ticket_description"]
        permission = form_json["submission"]["ticket_allow"]
        state = json.loads(form_json["state"])
        team = state["name"]
        try:
            if permission == "Yes":
                slck.new_ticket_message_public(user, description, team)
            else:
                slck.new_ticket_message_private()
        except Exception:
            return "", 400

    return "", 200


# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
