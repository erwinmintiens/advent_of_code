"""--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

ANSWER: 528799

--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

ANSWER = 84907174
"""

import re


def read_input(file_name: str) -> list:
    with open(file_name, "r") as myfile:
        lines = [line.strip() for line in myfile]
    return lines


def get_numbers_from_line(line: str) -> list[dict]:
    indexes = [(m.start(0), m.end(0)) for m in re.finditer("\d+", line)]
    result = []
    for item in indexes:
        result.append(
            {
                "value": int(line[item[0] : item[1]]),
                "starting_index": item[0],
                "ending_index": item[1],
            }
        )
    return result


NUMBERS_WITH_DOT = "0123456789."


def check_if_symbol_surrounds_number(
    lines: list, current_index: int, starting_index: int, ending_index: int
) -> bool:
    for index in range(starting_index - 1, ending_index + 1):
        try:
            if lines[current_index - 1][index] not in NUMBERS_WITH_DOT:
                return True
        except IndexError:
            pass
        try:
            if lines[current_index + 1][index] not in NUMBERS_WITH_DOT:
                return True
        except IndexError:
            pass
    try:
        if lines[current_index][starting_index - 1] not in NUMBERS_WITH_DOT:
            return True
    except IndexError:
        pass
    try:
        if lines[current_index][ending_index] not in NUMBERS_WITH_DOT:
            return True
    except IndexError:
        pass
    return False


def part1():
    lines = read_input("input_files/input_day_3.txt")
    result = 0
    for index, line in enumerate(lines):
        numbers = get_numbers_from_line(line)
        for item in numbers:
            if check_if_symbol_surrounds_number(
                lines, index, item["starting_index"], item["ending_index"]
            ):
                result += item["value"]
    print(result)


def find_all_asterisks_in_line(line: str):
    return [index for index, value in enumerate(line) if value == "*"]


def handle_asterisk(asterisk_index: int, current_line_index: int, lines: list):
    numbers_next_to_asterisk = []
    numbers_previous_line = get_numbers_from_line(lines[current_line_index - 1])
    numbers_current_line = get_numbers_from_line(lines[current_line_index])
    numbers_next_line = get_numbers_from_line(lines[current_line_index + 1])
    for item in numbers_previous_line:
        if (
            item["starting_index"] >= asterisk_index + 2
            or item["ending_index"] <= asterisk_index - 1
        ):
            continue
        numbers_next_to_asterisk.append(item)
    for item in numbers_current_line:
        if (
            item["starting_index"] == asterisk_index + 1
            or item["ending_index"] == asterisk_index
        ):
            numbers_next_to_asterisk.append(item)
    for item in numbers_next_line:
        if (
            item["starting_index"] >= asterisk_index + 2
            or item["ending_index"] <= asterisk_index - 1
        ):
            continue
        numbers_next_to_asterisk.append(item)
    return numbers_next_to_asterisk


def part2():
    lines = read_input("input_files/input_day_3.txt")
    result = 0
    for index, line in enumerate(lines):
        asterisks = find_all_asterisks_in_line(line)
        for asterisk in asterisks:
            numbers_next_to_asterisk = handle_asterisk(asterisk, index, lines)
            if len(numbers_next_to_asterisk) > 1:
                mult = 1
                for x in numbers_next_to_asterisk:
                    mult = x["value"] * mult
                result += mult
    print(result)
    return


if __name__ == "__main__":
    part1()
    part2()
