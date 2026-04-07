import sys
import parsing
import draw 
from random import randint, choice


def main() -> None:

    if len(sys.argv) != 2:
        print("[ERROR] Invalid input. Only takes one argument")
        sys.exit()
    config_dict = parsing.parsing_keys()
    if isinstance(config_dict, str):
        print(config_dict)
        sys.exit()
    number_coordinates = parsing.get_42_coordinates(config_dict)
    try:
        parsing.parsing_values(config_dict, number_coordinates)
    except ValueError as message:
        print(message)
        sys.exit()
    height = config_dict["height"]
    width = config_dict["width"]
    maze_info = create_maze(width, height, number_coordinates)
    write_output(config_dict["output_file"], config_dict["width"], maze_info)
    draw.main(config_dict, number_coordinates)


def get_possible_moves(width: int, height: int, curr_coordinate: tuple[int, int],
                       taken_coordinates: list[tuple[int, int]]) -> list[int]:

    x, y = curr_coordinate
    up = (x, y - 1)
    right = (x + 1, y)
    down = (x, y + 1)
    left = (x - 1, y)
    moves_dict = {0: up, 1: right, 2: down, 3: left}
    possible_moves = []
    for move in moves_dict.values():
        x, y = move
        if (x >= 0 and x < width and
            y >= 0 and y < height and
            move not in taken_coordinates):
            possible_moves.append(move)
    possible_moves_dict = {num: move for num, move in moves_dict.items() if
                           move in possible_moves}
    return (possible_moves_dict)


def create_maze(width: int, height: int,
                number_coordinates: list[tuple[int, int]]) -> dict[tuple[int, int],
                                                                   list[int]]:

    grid = dict()
    for i in range(height):
        for j in range(width):
            grid[(j, i)] = [1, 1, 1, 1]
    curr_coordinate = (0, 0)
    moves_made = [curr_coordinate]
    taken_coordinates = number_coordinates + moves_made
    total_cells = len(grid)
    while len(taken_coordinates) != total_cells:
        possible_moves_dict = get_possible_moves(width, height, curr_coordinate,
                                                 taken_coordinates)
        while not possible_moves_dict:
            moves_made.pop()
            curr_coordinate = moves_made[-1]
            possible_moves_dict = get_possible_moves(width, height, curr_coordinate,
                                                     taken_coordinates)
        index = choice(list(possible_moves_dict.keys()))
        grid[curr_coordinate][index] = 0
        curr_coordinate = possible_moves_dict[index]
        grid[curr_coordinate][(index + 2) % 4] = 0
        moves_made.append(curr_coordinate)
        taken_coordinates.append(curr_coordinate)
    return (grid)


def write_output(filename: str,
                 width: int,
                 grid: dict[tuple[int, int], list[int]]) -> None:

    file = open(filename, 'w')
    for cell, doors_config in grid.items():
        x, y = cell
        up, right, down, left = doors_config
        number = up + right * 2 + down * 4 + left * 8
        if number < 10:
            file.write(str(number))
        else:
            leftover = number - 10
            file.write(chr(ord('A') + leftover))
        if x == width - 1:
            file.write("\n")
    file.close()


if __name__ == "__main__":
    main()
