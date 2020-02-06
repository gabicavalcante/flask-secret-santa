from app.bot import process_message, _send_message
from twilio.rest import Client
from app.models import Draw
from dynaconf import settings
import mock


def _send_message_mock(message, number):
    """
    mock the send message   
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    body = "\n".join(message)
    message = client.messages.create(
        body=body, from_=settings.TWILIO_WHATSAPP, to=number
    )


def test_process_message_help():
    xml_response = """<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message><Body>'get draws' - get information about all draws that you make parte.\n'create draw' - start create a new draw\n'run draw' - run the draw</Body></Message></Response>"""
    assert process_message("help", settings.TWILIO_WHATSAPP) == xml_response


@mock.patch("app.bot._send_message", side_effect=_send_message_mock)
def test_get_response_create_draw(mock_function):
    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>Hey! You created a new draw!\nThe draw code is 1\nGive to your friends this code.\nWhen they finish, texting \'run draw {draw.id}\'.</Body></Message></Response>"""
    assert process_message("create draw", settings.TWILIO_WHATSAPP) == xml_response

    draw = Draw.query.filter_by(responsible_number=settings.TWILIO_WHATSAPP).first()
    assert draw
    assert draw.in_process

    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>{0} was add!</Body></Message></Response>"""
    assert process_message(
        "Bill want to join the draw 1", "+5571981265131"
    ) == xml_response.format("Bill")

    assert process_message(
        "Ana want to join the draw 1", "+5571981265132"
    ) == xml_response.format("Ana")

    assert len(draw.participants) == 2

    assert draw.run() == [(draw.participants[0], draw.participants[1])]

    # assert draw.run() == [(draw.participants[0], draw.participants[1])]
    # assert get_response("run draw", settings.TWILIO_WHATSAPP, draw) == ["draw done!"]

