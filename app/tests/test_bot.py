from app.bot import process_message
from flask import current_app
from twilio.rest import Client
from app.models import Draw, Participant
from dynaconf import settings
import mock


def _send_message_mock(message, number):
    """
    Mock function to replace the _send_message.
    In this function we use a different twilio number in
    from_ field to make requests with test credentials.
     
    :param message: message to send
    :param message: twilio test phone number
    """
    client = Client(
        current_app.config["TWILIO_ACCOUNT_SID"],
        current_app.config["TWILIO_AUTH_TOKEN"],
    )

    body = "\n".join(message)
    message = client.messages.create(
        body=body, from_=current_app.config["TWILIO_WHATSAPP"], to=number
    )


def test_process_message_help(app):
    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>*create draw* - start create a new draw\n*run draw* - run the draw</Body></Message></Response>"""
    assert process_message("help", settings.TWILIO_WHATSAPP) == xml_response


@mock.patch("app.bot._send_message", side_effect=_send_message_mock)
def test_response_create_draw(mock_function):
    # create a new draw
    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>Hey! You created a new draw!\n*The draw code is 1*\nGive to your friends this code.\nWhen they finish, texting \'run draw {draw.id}\'.</Body></Message></Response>"""
    assert process_message("create draw", settings.TWILIO_WHATSAPP) == xml_response

    draw = Draw.query.filter_by(responsible_number=settings.TWILIO_WHATSAPP).first()
    assert draw
    assert draw.in_process

    # add participants
    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>*{0}* was added!</Body></Message></Response>"""
    assert process_message(
        "Bill want to join the draw 1", "+5571981265131"
    ) == xml_response.format("Bill")

    assert process_message(
        "Ana want to join the draw 1", "+5571981265132"
    ) == xml_response.format("Ana")

    assert len(draw.participants) == 2

    # run the draw
    result = draw.run()
    assert not draw.in_process
    assert (draw.participants[0], draw.participants[1]) in result
    assert (draw.participants[1], draw.participants[0]) in result

    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>Draw {0} is not open.</Body></Message></Response>"""
    assert process_message("run draw 1", "+5571981265132") == xml_response.format(
        draw.id
    )


def test_run_draw(app):
    participant1 = Participant(name="Ana", number="5571981265131")
    participant2 = Participant(name="Bil", number="5571981265132")
    participant3 = Participant(name="Carl", number="5571981265133")
    participant4 = Participant(name="Katy", number="5571981265144")
    participant5 = Participant(name="Phil", number="5571981265155")

    draw = Draw(responsible_number=settings.TWILIO_WHATSAPP, in_process=True)
    draw.participants.extend(
        [participant1, participant2, participant3, participant4, participant5]
    )

    result = draw.run()
    assert len(result) == 5
    participants1 = [
        participant1,
        participant2,
        participant3,
        participant4,
        participant5,
    ]
    participants2 = [
        participant1,
        participant2,
        participant3,
        participant4,
        participant5,
    ]

    for pair in result:
        p1, p2 = pair
        participants1.remove(p1)
        participants2.remove(p2)

    assert not participants1
    assert not participants2
