import re
from collections import namedtuple

import click
from lib import Rover

Plateau = namedtuple("Plateau", ["x", "y"])


def parse_plateau(input):
    s = re.match("Plateau:([0-9]+) ([0-9]+)$", input)
    if not s:
        raise ValueError(f"Invalid plateau input data. The error input: {input}")
    return Plateau(int(s.group(1)), int(s.group(2)))


def parse_rover_landing_position(input):
    s = re.match(
        "Rover[0-9]+ Landing:([0-9]+) ([0-9]+) (N|E|S|W)",
        input,
    )
    if not s:
        raise ValueError(f"Invalid rover landing input. The error input: {input}")
    return (int(s.group(1)), int(s.group(2)), s.group(3))


def parse_instruction(input):
    s = re.match("Rover[0-9]+ Instructions:((L|R|M)+)$", input)
    if not s:
        raise ValueError(
            f"""Invalid rover instruction. It must contain only ('L','R','M')."""
            f"""The error input: {input}"""
        )
    return s.group(1)


@click.command()
@click.argument("input", type=click.File("r"))
def cli(input):
    lines = input.readlines()

    if not len(lines) % 2 == 1:
        print("The line count of the input file should be odd number.")
        return

    rovers = []

    try:
        plateau = parse_plateau(lines[0])

        for i in range(1, int(len(lines) / 2) + 1):
            rover_landing = lines[2 * i - 1]
            rover_instruction = lines[2 * i]

            x, y, cardinal = parse_rover_landing_position(rover_landing)
            instruction = parse_instruction(rover_instruction)

            rover = Rover(x, y, cardinal, plateau.x, plateau.y)
            rover.move(instruction)
            rovers.append(rover)

    except Exception as e:
        print(e)
        return

    for c, rover in enumerate(rovers, 1):
        print(f"Rover {c}:{rover}")

    return
