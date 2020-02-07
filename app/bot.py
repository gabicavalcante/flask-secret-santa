from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from app.models import db, Draw, Participant
from dynaconf import settings


def _send_message(message, number):
    """
    send a whatsapp message
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    body = "\n".join(message)
    message = client.messages.create(
        body=body,
        from_=f"whatsapp:{settings.TWILIO_WHATSAPP}",
        to=f"whatsapp:{number}",
    )


def _bot_replay(response):
    """
    replay the whatpsapp message
    """
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("\n".join(response))
    return str(resp)


def process_message(message, number):
    """
    process the user message
    """
    response = []

    # help command
    if message == "help":
        response.append("*create draw* - start create a new draw")
        response.append("*run draw* - run the draw")
        return _bot_replay(response)

    if message == "create draw":
        draw = Draw.create(responsible_number=number)
        db.session.add(draw)
        db.session.commit()

        response.append("Hey! You created a new draw!")
        response.append(f"*The draw code is {draw.id}*")
        response.append("Give to your friends this code.")
        response.append("When they finish, texting 'run draw {draw.id}'.")

        return _bot_replay(response)

    if "want to join the draw" in message:
        participant_name = message.split("want to join the draw")[0].strip()
        code = message.split("want to join the draw")[-1].strip()
        draw = Draw.query.filter_by(id=code).first()

        if not draw:
            response.append(f"There is not draw with code {code}!")
            response.append(
                f"Please, send a message in the form '*NAME* want to join the draw *CODE*'"
            )
            response.append("For example, 'Bill want to join the draw 9'")
            return _bot_replay(response)

        participant = Participant.find_or_create(participant_name, number)
        draw.participants.append(participant)
        db.session.add(participant)
        db.session.commit()

        response.append(f"*{participant_name}* was add!")

        _send_message(response, draw.responsible_number)
        return _bot_replay(response)

    if "run draw" in message:
        code = message.split("run draw")[-1]
        draw = Draw.query.filter_by(id=code).first()
        if not draw:
            response.append(f"There is not draw with code {code}!")
            response.append(f"Please, send a message in the form 'run draw {code}'")
            response.append("For example, 'run draw 9'")
            return _bot_replay(response)

        if not draw.in_process:
            response.append(f"Draw {draw.id} is not open.")
            return _bot_replay(response)

        result = draw.run()
        db.session.commit()
        for pair in result:
            p1, p2 = pair
            _send_message(
                [f"Hi {p1.name}, you got {p2.name} ({p2.number})!"], p1.number,
            )

        return _bot_replay(["draw is done!"])
    return _bot_replay(["Sorry, I can't help you :("])
