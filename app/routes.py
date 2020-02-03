from flask import Blueprint, request
from app.bot import get_response, send_message

bot = Blueprint("bot", __name__)


@bot.route("/bot", methods=["POST"])
def index():
    incoming_msg = request.values.get("Body", "").strip().lower()
    remote_number = request.values.get("From", "")

    if remote_number.startswith("whatsapp:"):
        remote_number = remote_number.split(":")[1]

    response = get_response(incoming_msg)
    send_message(response)
    return response
