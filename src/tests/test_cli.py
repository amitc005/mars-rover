import pytest

from ..cli import parse_instruction
from ..cli import parse_plateau
from ..cli import parse_rover_landing_position


class TestRoverCLI:
    @pytest.mark.parametrize(
        "input, expected",
        [
            ("Rover1 Instructions:LMR", "LMR"),
            ("Rover1 Instructions:MRMRMRMRMR", "MRMRMRMRMR"),
            ("Rover1 Instructions:LLLLLLLLL", "LLLLLLLLL"),
        ],
    )
    def test_parse_instruction(self, input, expected):
        instruction = parse_instruction(input)

        assert instruction == expected

    @pytest.mark.parametrize(
        "input",
        [
            # Lack of the rover number
            "Rover Instructions:LMR",
            # Invalid instruction character like X
            "Rover1 Instructions:LMRXYZ",
            # Lack of the colon between the description and the instruction
            "Rover1 Instructions LLLLLLLLL",
            # Extra value after the instruction.
            "Rover1 Instructions:LLLLLLLLL Test1234",
        ],
    )
    def test_parse_invalid_instruction(self, input):
        with pytest.raises(ValueError):
            parse_instruction(input)

    @pytest.mark.parametrize(
        "input, expected_x, expected_y",
        [
            ("Plateau:10 10", 10, 10),
            ("Plateau:100000 100000", 100000, 100000),
            ("Plateau:5 5", 5, 5),
            ("Plateau:0 0", 0, 0),
        ],
    )
    def test_parse_plateau(self, input, expected_x, expected_y):
        plateau = parse_plateau(input)

        assert plateau.x == expected_x
        assert plateau.y == expected_y

    @pytest.mark.parametrize(
        "input",
        [
            ("Plateau10 10"),
            ("Plateau:-1 -1"),
            ("Plateau:-1 5"),
            ("Plateau:5 -1"),
            ("Plateau:5 -1 invalid character"),
        ],
    )
    def test_parse_invalid_plateau(self, input):
        with pytest.raises(ValueError):
            parse_plateau(input)

    @pytest.mark.parametrize(
        "input, expected_x, expected_y, expected_cardinal",
        [
            ("Rover1 Landing:1 2 N", 1, 2, "N"),
            ("Rover2 Landing:5 5 S", 5, 5, "S"),
            ("Rover3 Landing:10 10 E", 10, 10, "E"),
            ("Rover4 Landing:10 10 W", 10, 10, "W"),
        ],
    )
    def test_parse_landing_position(
        self, input, expected_x, expected_y, expected_cardinal
    ):
        (x, y, cardinal) = parse_rover_landing_position(input)

        assert x == expected_x
        assert y == expected_y
        assert cardinal == expected_cardinal

    @pytest.mark.parametrize(
        "input",
        [
            "Rover1 Landing1 2 N",
            "Rover2 Landing:-5 5 S",
            "Rover3 Landing:10 -10 E",
            "Rover4 Landing:10 10 X",
        ],
    )
    def test_parse_invalid_landing_position(self, input):
        with pytest.raises(ValueError):
            parse_rover_landing_position(input)
