from app.bot import process_message
from app.models import SecretSanta, Participant 


def test_process_message_help(app):
    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>create: create a new secret santa\nrun {code}: run the secret santa\ncancel {code}: cancel the secret santa\nadd {name} to {code}: to join the secret santa</Body></Message></Response>"""
    assert process_message("help", app.config.TWILIO_NUMBER) == xml_response


def test_response_create_draw(app):
    # create a new secretsanta
    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>Hey! You created a new Secret Santa!\n*The Secret Santa code is 1*\nGive to your friends this code.\nWhen they finish, texting \'run 1\'.</Body></Message></Response>"""
    assert process_message("create", app.config.TWILIO_NUMBER) == xml_response

    secretsanta = SecretSanta.query.filter_by(
        creator_number=app.config.TWILIO_NUMBER
    ).first()
    assert secretsanta
    assert secretsanta.in_process

    # add participants
    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>*{0}* was added!</Body></Message></Response>"""
    assert process_message("add Bill to 1", "+5571981265131") == xml_response.format(
        "Bill"
    )

    assert process_message("add Ana to 1", "+5571981265132") == xml_response.format(
        "Ana"
    )

    assert len(secretsanta.participants) == 2

    # run the secretsanta
    result = secretsanta.run()
    assert not secretsanta.in_process
    assert (secretsanta.participants[0], secretsanta.participants[1]) in result
    assert (secretsanta.participants[1], secretsanta.participants[0]) in result

    xml_response = """<?xml version="1.0" encoding="UTF-8"?><Response><Message><Body>Secret Santa {0} is not open.</Body></Message></Response>"""
    assert process_message("run 1", "+5571981265132") == xml_response.format(
        secretsanta.id
    )


def test_run_draw(app):
    participant1 = Participant(name="Ana", number="5571981265131")
    participant2 = Participant(name="Bil", number="5571981265132")
    participant3 = Participant(name="Carl", number="5571981265133")
    participant4 = Participant(name="Katy", number="5571981265144")
    participant5 = Participant(name="Phil", number="5571981265155")

    secretsanta = SecretSanta(creator_number=app.config.TWILIO_NUMBER, in_process=True)
    secretsanta.participants.extend(
        [participant1, participant2, participant3, participant4, participant5]
    )

    result = secretsanta.run()
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
