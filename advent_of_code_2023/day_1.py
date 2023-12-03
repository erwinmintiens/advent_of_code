"""--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

ANSWER: 53921

--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

"""

import re


NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}


def read_input(file_name: str) -> list:
    with open(file_name, "r") as myfile:
        lines = [line.strip() for line in myfile]
    return lines


def get_first_and_last_number(lines: list):
    result = 0
    for line in lines:
        number = get_numbers(line)
        print(f"{line=}")
        print(f"{number=}")
        result += number
    return result


def get_first_number_from_line(line: str) -> str:
    for char in line:
        result = check_if_character_is_number(char)
        if result:
            return result
    return ""


def get_last_number_from_line(line: str) -> str:
    for index, char in enumerate(line[::-1]):
        result = check_if_character_is_number(char)
        if result:
            return result
    return ""


def check_if_character_is_number(char: str) -> str | None:
    if char in "0123456789":
        return char


def get_numbers(line: str):
    highest_value = 0
    lowest_value = 0
    highest_index = None
    lowest_index = None
    for number in NUMBERS:
        if number in line:
            if highest_index is None:
                highest_index = get_highest_index(line, number)
                highest_value = NUMBERS[number]
            elif (
                highest_index is not None
                and get_highest_index(line, number) > highest_index
            ):
                highest_index = get_highest_index(line, number)
                highest_value = NUMBERS[number]
            if lowest_index is None:
                lowest_index = line.index(number)
                lowest_value = NUMBERS[number]
            elif lowest_index is not None and line.index(number) < lowest_index:
                lowest_index = line.index(number)
                lowest_value = NUMBERS[number]

    return int(lowest_value + highest_value)


def get_highest_index(line: str, value):
    index = 0
    for m in re.finditer(value, line):
        index = m.start()
    return index


def get_last_number(line: str):
    value = None
    highest_index = 0
    for number in NUMBERS[::-1]:
        if number in line and line.index(number) > highest_index:
            highest_index = line.index(number)
            value = number
    return value


if __name__ == "__main__":
    input = read_input("input_day_1.txt")
    # input = [
    #     "617rdpbn6",
    #     # "dtlqxk5six",
    #     "eightnine2eightnineeight",
    #     "v2oneonegxdngmtv",
    #     "4bf6rfnfive",
    # ]
    print(get_first_and_last_number(input))
