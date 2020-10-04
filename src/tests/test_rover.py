import pytest

from ..lib import ErrorMessage
from ..lib import Rover


class TestRover:
    @pytest.mark.parametrize(
        "x, y, cardinal, max_x, max_y, instructions, expected",
        [
            (1, 2, "N", 5, 5, "LMLMLMLMM", "1 3 N"),
            (1, 2, "n", 5, 5, "lmlmlmlmm", "1 3 N"),
            (3, 3, "E", 5, 5, "MMRMMRMRRM", "5 1 E"),
            (3, 3, "e", 5, 5, "mmrmmrmrrm", "5 1 E"),
        ],
    )
    def test_first_example(self, x, y, cardinal, max_x, max_y, instructions, expected):
        rover = Rover(x, y, cardinal, max_x, max_y)
        rover.move(instructions)

        assert expected == str(rover)

    @pytest.mark.parametrize(
        "x, y, cardinal, max_x, max_y, instructions, error_inst",
        [
            (1, 2, "N", 5, 5, "INVALID_INSTRUCTIONS", "I"),
            (1, 2, "N", 5, 5, "LM123456789", "1"),
            (1, 2, "N", 5, 5, "LM!LM@#$$%^&*", "!"),
        ],
    )
    def test_invalid_instructions(
        self, x, y, cardinal, max_x, max_y, instructions, error_inst
    ):
        rover = Rover(x, y, cardinal, max_x, max_y)
        with pytest.raises(ValueError) as excinfo:
            rover.move(instructions)
        expected_error_message = ErrorMessage.UNKNOWN_INSTRUCTION_VALUE % error_inst
        assert str(excinfo.value) == expected_error_message

    @pytest.mark.parametrize(
        "x, y, cardinal, max_x, max_y, instructions",
        [
            (6, 2, "N", 5, 5, "LMLMLMLMM"),
            (5, 6, "E", 5, 5, "MMRMMRMRRM"),
            (-1, 3, "E", 5, 5, "MMRMMRMRRM"),
            (1, -1, "E", 5, 5, "MMRMMRMRRM"),
        ],
    )
    def test_invalid_rover_position(self, x, y, cardinal, max_x, max_y, instructions):
        rover = Rover(x, y, cardinal, max_x, max_y)
        with pytest.raises(ValueError) as excinfo:
            rover.move(instructions)
        assert str(excinfo.value) == ErrorMessage.ROVER_OUT_OF_RANGE
