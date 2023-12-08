"""--- Day 8: Haunted Wasteland ---

You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

ANSWER: 21797

--- Part Two ---

The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the instructions, but you've barely left your starting position. It's going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?

"""


class Called:
    def __init__(self, instruction_index: int, direction_number: int) -> None:
        self.instruction_index = instruction_index
        self.direction_number = direction_number


class Node:
    def __init__(
        self,
        value: str,
        left: str,
        right: str,
        called_at_instruction_index: list[Called] = [],
    ) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.called_at_instruction_index = called_at_instruction_index

    def __repr__(self) -> str:
        return f"Node {self.value} [{self.left}, {self.right}]"


def find_node_from_value(nodes_list: list[Node], node_value: str) -> Node:
    return [item for item in nodes_list if item.value == node_value][0]


def find_next_node_value(current_node: Node, instruction: str) -> str:
    return current_node.left if instruction == "L" else current_node.right


def find_next_node_value_from_value(
    node_value: str, instruction: str, nodes_list: list[Node]
) -> str:
    node = find_node_from_value(nodes_list, node_value)
    return find_next_node_value(node, instruction)


def transform_lines_to_nodes(lines: list) -> list[Node]:
    return [transform_line_to_node(line) for line in lines if "=" in line]


def execute_part_1(
    nodes_list: list[Node],
    instructions: str,
    node_value: str = "AAA",
    current_instruction_index=0,
) -> tuple[int, str, int]:
    number_of_directions = 0
    if node_value.endswith("Z"):
        node = next(item for item in nodes_list if item.value == node_value)
        try:
            instruction = instructions[current_instruction_index]
        except IndexError:
            instruction = instructions[0]
            current_instruction_index = 0
        node_value = find_next_node_value(node, instruction)
        number_of_directions += 1
        current_instruction_index += 1
    while not node_value.endswith("Z"):
        node = next(item for item in nodes_list if item.value == node_value)
        try:
            instruction = instructions[current_instruction_index]
        except IndexError:
            instruction = instructions[0]
            current_instruction_index = 0
        node_value = find_next_node_value(node, instruction)
        number_of_directions += 1
        current_instruction_index += 1
    return number_of_directions, node_value, current_instruction_index


def find_offset_and_loop_length(
    nodes_list: list[Node], instructions: str, starting_node_value: str
) -> tuple[Node, int]:
    number_of_directions = 0
    current_instruction_index = 0
    current_node = find_node_from_value(nodes_list, starting_node_value)
    while True:
        try:
            instruction = instructions[current_instruction_index]
        except IndexError:
            instruction = instructions[0]
            current_instruction_index = 0
        if next(
            (
                item
                for item in current_node.called_at_instruction_index
                if item.instruction_index == current_instruction_index
            ),
            None,
        ):
            return current_node, number_of_directions
        current_node.called_at_instruction_index.append(
            Called(current_instruction_index, number_of_directions)
        )
        node_value = find_next_node_value_from_value(
            current_node.value, instruction, nodes_list
        )
        current_node = find_node_from_value(nodes_list, node_value)
        print(f"{current_node=}, {current_instruction_index=}")
        number_of_directions += 1
        current_instruction_index += 1


def transform_line_to_node(line: str):
    unpacked_line = [item.strip() for item in line.split("=")]
    value, next_nodes = unpacked_line[0], unpacked_line[1]
    unpacked_nodes = [
        item.replace("(", "").replace(")", "").strip() for item in next_nodes.split(",")
    ]
    left_node, right_node = unpacked_nodes[0], unpacked_nodes[1]
    return Node(value, left_node, right_node)


def read_input(file_name: str) -> list[str]:
    with open(file_name, "r") as myfile:
        lines = [line.strip() for line in myfile]
    return lines


def part1():
    lines = read_input("input_files/input_day_8.txt")
    nodes_list = transform_lines_to_nodes(lines)
    instructions = lines[0]
    number_of_directions, node_value, _ = execute_part_1(nodes_list, instructions)
    print(f"{number_of_directions=}, {node_value=}")


def part2():
    lines = read_input("input_files/input_day_8.txt")
    nodes_list = transform_lines_to_nodes(lines)
    instructions = lines[0]
    starting_node = next(item for item in nodes_list if item.value.startswith("A"))
    print(f"{starting_node=}")
    node, number_of_directions = find_offset_and_loop_length(
        nodes_list, instructions, starting_node.value
    )
    print(f"{node.called_at_instruction_index=}")
    print(f"{node}")
    print(f"{number_of_directions=}")


if __name__ == "__main__":
    part1()
    part2()
