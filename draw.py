from mlx import Mlx


def on_key(keycode, param):

    mlx, mlx_ptr = param
    print("mlx key:", keycode)
    if keycode == 65307:
        mlx.mlx_loop_exit(mlx_ptr)


def paint_pixel(buf: list[int], y: int, x: int, size_line: int,
                blue: int, green: int, red: int, trans: int) -> None:

    index = y * size_line + x * 4
    buf[index + 0] = blue
    buf[index + 1] = green
    buf[index + 2] = red
    buf[index + 3] = trans


def draw_maze(buf: list[int], config_dict: dict[str, any], number_coordinates: list[int],
              size_line: int, width: int, height: int, cell_size: int) -> None:

    
    # Draw the background in blue 
    for y in range(height):
        for x in range(width):
            paint_pixel(buf, y, x, size_line, 255, 0, 0, 255)

    # Draw the numbers 42
    for (x, y) in number_coordinates:
        x -= 1
        y -= 1
        for i in range(cell_size):
            for j in range(cell_size):
                paint_pixel(buf, y * cell_size + i, x * cell_size + j,
                            size_line, 0, 0, 0, 255)

    # Draw start and finish spots 
    x_start, y_start = config_dict["entry"]
    x_final, y_final = config_dict["exit"]
    x_start -= 1
    y_start -= 1
    x_final -= 1
    y_final -= 1
    for i in range(cell_size):
        for j in range(cell_size):
            paint_pixel(buf, y_start * cell_size + i, x_start * cell_size + j,
                        size_line, 0, 255, 0, 255)
            paint_pixel(buf, y_final * cell_size + i, x_final * cell_size + j,
                        size_line, 0, 0, 255, 255)

    # Draw the walls by reading the hexadecimal file 
    curr_x = 0
    curr_y = 0
    maze_file = open(config_dict["output_file"], 'r')
    while True:
        number_str = maze_file.read(1)
        if not number_str:
            break
        if number_str == "\n":
            curr_y += cell_size
            curr_x = 0
        else:
            try:
                number = int(number_str)
            except ValueError:
                number = 10 + ord(number_str) - ord('A')
            if number & 1:
                for x in range(cell_size):
                    paint_pixel(buf, curr_y, curr_x + x, size_line, 0, 0, 0, 255)
            if number & 2:
                for y in range(cell_size):
                    paint_pixel(buf, curr_y + y, curr_x + cell_size - 1, 
                                size_line, 0, 0, 0, 255)
            if number & 4:
                for x in range(cell_size):
                    paint_pixel(buf, curr_y + cell_size - 1, curr_x + x,
                                size_line, 0, 0, 0, 255)
            if number & 8:
                for y in range(cell_size):
                    paint_pixel(buf, curr_y + y, curr_x, size_line, 0, 0, 0, 255)
            curr_x += cell_size


def main(config_dict: dict[tuple[int, int], list[int]], 
         number_coordinates: list[tuple[int, int]]) -> None:

    cell_size = 25
    width, height = config_dict["width"] * cell_size, config_dict["height"] * cell_size
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win_ptr = mlx.mlx_new_window(mlx_ptr, width, height, "Maze Generator")

    img_ptr = mlx.mlx_new_image(mlx_ptr, width, height)
    buf, bpp, size_line, fmt = mlx.mlx_get_data_addr(img_ptr)

    draw_maze(buf, config_dict, number_coordinates, size_line, width, height, cell_size)
    
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

    mlx.mlx_key_hook(win_ptr, on_key, (mlx, mlx_ptr))
    mlx.mlx_loop(mlx_ptr)
