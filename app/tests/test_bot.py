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
        "Hey! You created a new draw!",
        "Now, you need to texting the name of the participants in the form {participant name}, {phone number}.",
        "For example 'Petter, +55 84 981231144'",
        "When you finish, texting 'run draw'.",
    ]

    draw = Draw.query.filter_by(responsible_number="981341213").first()

    assert get_response("Ana, 11111111", "981341213", draw) == ["Ana was add!"]
    assert get_response("Bil, 22222222", "981341213", draw) == ["Bil was add!"]

    assert len(draw.participants) == 2

    assert draw.run() == [(draw.participants[0], draw.participants[1])]
    assert get_response("run draw", "981341213", draw) == ["draw done!"]

    assert get_response("Carl, 33333333", "981341213", draw) == ["Carl was add!"]
    assert get_response("Lion, 44444444", "981341213", draw) == ["Lion was add!"]

    assert len(draw.run()) == 2

