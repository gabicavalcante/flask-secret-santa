from app.bot import get_response


def test_get_response_help():
    assert get_response("help", "981341213", None) == [
        "'get draws' - get information about all draws that you make parte.",
        "'create draw' - start create a new draw",
        "'run draw' - run the draw",
    ]


def test_get_response_create_draw():
    assert get_response("create draw", "981341213", None) == ""
