def read_input(file_name: str) -> list:
    with open(file_name, "r") as myfile:
        lines = [line.strip() for line in myfile]
    return lines
