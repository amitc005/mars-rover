from enum import Enum


class Instructor(Enum):
    SPIN_LEFT = "L"
    SPIN_RIGHT = "R"
    MOVE_FORWARD = "M"


class ErrorMessage:
    ROVER_OUT_OF_RANGE = "The rover is out of the plateau."
    UNKNOWN_INSTRUCTION_VALUE = "Unknown instruction value %s"


class Rover:
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    LEFT_SPINNER = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
    RIGHT_SPINNER = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}

    def __init__(self, x, y, cardinal, plateau_x, plateau_y):
        self.x = x
        self.y = y
        self.cardinal = cardinal.upper()
        self.max_x = plateau_x
        self.max_y = plateau_y

        self.instructors = {
            Instructor.SPIN_LEFT.value: self.spin_left,
            Instructor.SPIN_RIGHT.value: self.spin_right,
            Instructor.MOVE_FORWARD.value: self.move_forward,
        }

    def spin_left(self):
        self.cardinal = self.LEFT_SPINNER[self.cardinal]

    def spin_right(self):
        self.cardinal = self.RIGHT_SPINNER[self.cardinal]

    def move_forward(self):
        if self.cardinal == self.NORTH:
            self.y = self.y if self.y == self.max_y else self.y + 1
        elif self.cardinal == self.SOUTH:
            self.y = self.y if self.y == 0 else self.y - 1
        elif self.cardinal == self.EAST:
            self.x = self.x if self.x == self.max_x else self.x + 1
        elif self.cardinal == self.WEST:
            self.x = self.x if self.x == 0 else self.x - 1

    def move(self, instructions):
        if self.x > self.max_x or self.x < 0 or self.y > self.max_y or self.y < 0:
            raise ValueError(ErrorMessage.ROVER_OUT_OF_RANGE)

        for inst in instructions:
            try:
                self.instructors[inst.upper()]()
            except KeyError:
                raise ValueError(ErrorMessage.UNKNOWN_INSTRUCTION_VALUE % inst.upper())

    def __str__(self):
        return f"{self.x} {self.y} {self.cardinal}"
