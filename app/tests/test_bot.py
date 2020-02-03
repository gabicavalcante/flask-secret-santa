from app.bot import get_response
from app.models import Draw

def test_get_response_help():
    assert get_response("help", "981341213", None) == [
        "'get draws' - get information about all draws that you make parte.",
        "'create draw' - start create a new draw",
        "'run draw' - run the draw",
    ]


def test_get_response_create_draw():
    assert get_response("create draw", "981341213", None) == [
        "Create a new draw by texting the name of the participants in the form {participant name}, {phone number}.",
        "For example 'Petter, +55 84 981231144'",
        "When you finish, texting 'run draw'.",
    ]

    assert Draw.query.filter_by(responsable_number="981341213").first()