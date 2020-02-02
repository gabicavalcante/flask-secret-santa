from flask import Blueprint

bot = Blueprint("bot", __name__, url_prefix="/bot")


@bot.route("/")
def index():
    return {"msg": "ok"}
