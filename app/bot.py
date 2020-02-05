from twilio.twiml.messaging_response import MessagingResponse
from app.models import db, Draw, Participant


def send_message(response):
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("\n".join(response))
    return str(resp)


def get_response(message, number, draw):
    response = []

    # Help commands
    if message == "help":
        response.append(
            "'get draws' - get information about all draws that you make parte."
        )
        response.append("'create draw' - start create a new draw")
        response.append("'run draw' - run the draw")
        return response

    if draw and draw.in_process and message == "run draw":
        draw.run()
        return ["draw done!"]

    if draw and draw.in_process:
        message_parts = message.split(",")
        if len(message_parts) != 2:
            response.append(
                "More than one / was sent. Please use only one / in message."
            )
            return response
        participant_name = message_parts[0].strip()
        participant_number = message_parts[1].strip()
        participant = Participant.find_or_create(participant_name, participant_number)
        db.session.add(participant)

        draw.participants.append(participant)
        db.session.commit()

        response.append(f"{participant_name} was add!")
        return response

    if message == "create draw":
        response.append("Hey! You created a new draw!")
        response.append(
            "Now, you need to texting the name of the participants in the form {participant name}, {phone number}."
        )
        response.append("For example 'Petter, +55 84 981231144'")
        response.append("When you finish, texting 'run draw'.")

        Draw.create(responsible_number=number)
        db.session.commit()

        return response
