import os
import time
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

#from product.pdf_generator_scripts.pdf_generator import get_data
from product.cut_optimizer.helpers import set_ticks
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


X = 3000    
Y = 3000
SAW = 3.2

X_IN = X / 25.4
Y_IN = Y / 25.4

id = 62

output_dir = f"/home/dylan/AutoWood/AutoWood_Backend/product/cut_optimizer/optimized_cuts/{id}"
optc_name = f"optc_{id}.png"
file_path = os.path.join(output_dir, optc_name)
fig, ax = plt.subplots(figsize=(12.8, 7.2))


class Board:

    def __init__(self, X, Y, x, y):
        self.X = X  # Width of the row
        self.Y = Y  # Height of the row
        self.start_x = x  # Starting x position
        self.start_y = y  # Starting y position
        self.occupied = False # is the Board occupied ?

    
    def space_check(self,format_width, format_height):

        if self.X < format_width or self.Y < format_height:    
            return False
        else:
            return True


    def __str__(self):
        return f"Board information X: {self.X}, Y: {self.Y}, start_x: {self.start_x}, start_y: {self.start_y}, Occupied: {self.occupied}"
    

    
                  
def add_format(board, format_width, format_height):
       
        if board.space_check(format_width,format_height) == True:

            print(f"Adding format: Width:{format_width}, Height: {format_height}")
            board.occupied = True
            return True          
        else:
            print("Not enough space in this BOARD")
            return False



def cut_first_board(boards,board,format_width, format_height):

    # Return the remaining size of the board in the same Y
    remaining_Y = board.Y - format_height - SAW
    new_board_start_y = board.start_y + format_height + SAW 
    remaining_X = board.X - format_width - SAW
    new_board_start_x = board.start_x + format_width + SAW
    print(f"remaining_y: {remaining_Y},new_board_start_y: {new_board_start_y}\nremaining_X: {remaining_X},new_board_start_x: {new_board_start_x}")

    # CUT
    #print(f"Before cut self.Y: {self.Y}")
    board.Y = format_height
    #print(f"After cut self.Y: {self.Y} ")
    board.X = format_width

    # Create new board in the same ROW
    new_board_same_row = Board(remaining_X,board.Y, new_board_start_x, 0)
    # Create new board above the row
    new_board_higher_row = Board(X, remaining_Y, 0, new_board_start_y)

    boards.append(new_board_higher_row)
    boards.append(new_board_same_row )

def cut_next_board(boards,board,format_width, format_height):

    # Return the remaining size of the board in the same Y
    remaining_Y = board.Y - format_height - SAW
    if remaining_Y < 0 or remaining_Y > Y:
        print("Halo blont")
    new_board_start_y = board.start_y + format_height + SAW 
    remaining_X = board.X - format_width - SAW
    new_board_start_x = board.start_x + format_width + SAW
    print(f"remaining_y: {remaining_Y},new_board_start_y: {new_board_start_y}\nremaining_X: {remaining_X},new_board_start_x: {new_board_start_x}")

    # CUT
    #print(f"Before cut self.Y: {self.Y}")
    board.Y = format_height
    #print(f"After cut self.Y: {self.Y} ")
    board.X = format_width

    # Create new board in the same ROW
    
    if (remaining_X + board.start_x) < X:
        new_board_same_row = Board(remaining_X, board.Y, new_board_start_x, board.start_y)
        boards.append(new_board_same_row )

        
    # Create new board above the row
    if remaining_Y > 0 or remaining_Y < Y and remaining_Y > 40:
        new_board_higher_row = Board(X, remaining_Y, board.start_x, new_board_start_y)
        boards.append(new_board_higher_row)
    
    
    

def format_fit_check(boards, width, height):

    #function to check if format fits any unoccupied board

    #if one board left
    if isinstance(boards,Board) and boards.X >= width and boards.Y >= height and boards.occupied == False : # Single board case
        draw_gaps(boards)
        return True

    #if more than 1 board
    elif isinstance(boards, list):
        for board in boards:
            if isinstance(board, Board):
                           
                
                print(f"Format fit check: width {width}, height {height}")
                if board.X >= width and board.Y >= height and board.occupied == False:
                    print(f"Format fit in this row: {board}")
                    return True
                else:
                    print(f"Format of sizes X{width} Y{height}  doesnt fit this row: {board}")
                    return False

        else:
            raise TypeError(f"Invalid input {type(boards).__name__}")
    return False

    
def scan_boards(boards):
    #function to scan free spaces on the board and mark free areas on the board for debug purposes

    if isinstance(boards,Board): # Single board case
        draw_gaps(boards)
    elif isinstance(boards, list):
        for board in boards:
            if isinstance(board, Board):
                draw_gaps(board)
            else:
                raise ValueError(f"Expected a Board got {type(board).__name__}")
    else:
        raise TypeError(f"Invalid input type {type(boards).__name__}")

def generate_board(X,Y):

    ax.set_xlim(0, X)
    ax.set_ylim(0, Y)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title("Rozkroje")
    x_ticks = set_ticks(X, 100)
    y_ticks = set_ticks(Y, 100)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    #project_data = get_data(id)
    #formats = convert_elements(project_data)
    #
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    formats = [[1200, 430], [1200, 430], [767,430], [767,430], [332,106], [332,106], [332,106],[1200, 430], [1200, 430], [767,430], [767,430], [332,106], [332,106], [332,106], [2005, 168], [2005, 168], [2005, 168], [2005, 168]]
    formats.sort(reverse=True)

    place_elements(formats)
    #print(formats)
    
    plt.savefig(file_path, format='png', dpi=150)

    

def convert_elements(project_data):

    elements = project_data["elements"]

    formats = []


    for element in elements:
        length = element['element']['dimX']
        width = element['element']['dimY']
        quantity = element['quantity']
        starting_x = 0
        starting_y = 0

        row = [length, width, starting_x, starting_y]

        for _ in range(int(quantity)):
            formats.append(row)

    formats.sort(reverse=True)
    return formats

def generate_rectangle(start_position_x, start_position_y, width, height, ax):

    rect = patches.Rectangle(xy=(start_position_x,start_position_y), width=width, height=height, edgecolor='black', facecolor='#d3e2dc', antialiased=True, linewidth=None)
    ax.add_patch(rect)

    print(f"Placing rectangle in X:{start_position_x},Y:{start_position_y} format size:  X: {width} Y:{height}" )

    text_x = start_position_x + width / 2
    text_y = start_position_y + height / 2
    ax.text(text_x, text_y, f'{width} x {height}', ha='center', va='center', fontsize=10, color='black')

def draw_gaps(board):
    """
    Draws red boundary lines for all virtual rows on the board.
    """
 
        # Draw a red rectangle to represent the virtual row boundaries
    if board.occupied == False:
        edgecolor = 'green'
    else:
        edgecolor = 'red'
    rect = patches.Rectangle(
        xy=(board.start_x, board.start_y), 
        width=board.X, 
        height=board.Y, 
        edgecolor=edgecolor , 
        facecolor='none', 
        linestyle='--', 
        linewidth=1
    )
    ax.add_patch(rect)
    print(f"Drawing board boundary: Start X={board.start_x}, Y={board.start_y}, Width={board.X}, Height={board.Y}")

def draw_free_space(vrs, ax):
    """
    Draws red boundary lines for all virtual rows on the board.
    """
    for vr in vrs:
        # Draw a red rectangle to represent the virtual row boundaries
        rect = patches.Rectangle(
            xy=(vr.start_x, vr.start_y), 
            width=vr.X, 
            height=vr.Y, 
            edgecolor='green', 
            facecolor='none', 
            linestyle='--', 
            linewidth=1
        )
        ax.add_patch(rect)
        print(f"Drawing free space: Start X={vr.start_x}, Y={vr.start_y}, Width={vr.X}, Height={vr.Y}")

def place_elements(formats):

    # Create first board based on available boards
    board_1 = Board(X,Y,0,0)
    boards = []
    boards.append(board_1)

    # Cut the board based on the first format 
    width, height = formats[0][0],formats[0][1]
    #first cut assumes it works
    cut_first_board(boards,boards[0], width, height)
    add_format(boards[0], width, height)
    formats.pop(0)
    scan_boards(boards)
    plt.savefig(file_path, format='png', dpi=150)
    free_boards = [board for board in boards if not board.occupied]
    try:
        while formats:                
            free_boards.sort(key=lambda board: board.start_y)
            placement_successful = False
            
            for board in free_boards:
                width, height = formats[0][0],formats[0][1]
                if format_fit_check(board, width,height) and board.occupied == False:
                        
                        add_format(board, width,height)
                        cut_next_board(free_boards,board, width,height)
                        scan_boards(free_boards)
                        
                        plt.savefig(file_path, format='png', dpi=150)
                        time.sleep(0.2)
                        free_boards = list(filter(lambda board: not board.occupied, free_boards))
                        free_boards.sort(key=lambda board: board.start_y)
                        boards.append(board)
                                               
                        formats.pop(0)

                        placement_successful = True
                        break
            if not placement_successful:
                print(" ERROR No more space available on existing boards. Add more space")                
                print(f"Following formats ommited: {formats[0]}")
                formats.pop(0)

            if not free_boards:
                print("No more space available on any boards. Add more space.")
                break

                
                
    except Exception as e:
        print(f"An error occured: {e}")

    
    occupied_boards = [board for board in boards if board.occupied]
    for board in occupied_boards:
        generate_rectangle(board.start_x, board.start_y, board.X, board.Y, ax)
        plt.savefig(file_path, format='png', dpi=150)
        time.sleep(0.2) 


    plt.savefig(file_path, format='png', dpi=150)
                
      
    return 0


generate_board(X,Y)
