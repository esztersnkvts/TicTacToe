from tkinter import *

# Define the depth limit for the Minimax algorithm (adjust as needed)
MAX_DEPTH = 4


def clear_root():
    for widget in root.winfo_children():
        widget.destroy()


def reset():
    window.destroy()
    clear_root()
    main()


def exit_game():
    window.destroy()
    root.destroy()


def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def end_game_window():
    global window
    window = Tk()
    window.geometry('400x400')
    window.title('Tic Tac Toe')

    root.update_idletasks()  # Ensure the first window's dimensions are known
    x = root.winfo_x() + root.winfo_width() // 6
    y = root.winfo_y() + root.winfo_height() // 6

    # Create the second window and position it in the middle of the first window
    window.geometry(f"+{x}+{y}")

    # Calculate font size based on the window dimensions
    font_size = int(window.winfo_width() // 15)

    # Set the number of rows and columns
    for i in range(5):
        window.grid_rowconfigure(i, weight=1)
        window.grid_columnconfigure(i, weight=1)

    new_game_btn = Button(window, text='New Game', font=('bold', font_size), command=reset)
    new_game_btn.grid(row=2, column=2, sticky='s')

    exit_btn = Button(window, text='Exit', font=('bold', font_size), command=exit_game)
    exit_btn.grid(row=3, column=2)


def disable_all_buttons():
    for row in buttons:
        for button in row:
            button.config(state="disabled")


def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']


def minimax(board, depth, is_maximizing):
    if check_win(board, ai_symbol):
        return 1
    if check_win(board, user_symbol):
        return -1
    if len(get_empty_cells(board)) == 0 or depth == MAX_DEPTH:
        return 0

    if is_maximizing:
        max_val = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = ai_symbol
                    val = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    max_val = max(max_val, val)
        return max_val
    else:
        min_val = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = user_symbol
                    val = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    min_val = min(min_val, val)
        return min_val


def best_move():
    best_score = -float("inf")
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = ai_symbol
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move


def ai():
    ai_row, ai_col = best_move()
    buttons[ai_row][ai_col].config(text=ai_symbol, state='disabled')
    board[ai_row][ai_col] = ai_symbol
    if check_win(board, ai_symbol):
        end_game_window()
        font_size = int(window.winfo_width() // 10)
        text = Label(window, text='You lost!', font=('bold', font_size))
        text.grid(row=1, column=2)
        disable_all_buttons()
    elif len(get_empty_cells(board)) == 0:
        end_game_window()
        font_size = int(window.winfo_width() // 10)
        text = Label(window, text='Draw!', font=('bold', font_size))
        text.grid(row=1, column=2)


def user_move(row, col):
    buttons[row][col].config(text=user_symbol, state='disabled')
    board[row][col] = user_symbol
    if check_win(board, user_symbol):
        end_game_window()
        font_size = int(window.winfo_width() // 10)
        text = Label(window, text='You won!', font=('bold', font_size))
        text.grid(row=1, column=2)
        disable_all_buttons()
    elif len(get_empty_cells(board)) == 0:
        end_game_window()
        font_size = int(window.winfo_width() // 10)
        text = Label(window, text='Draw!', font=('bold', font_size))
        text.grid(row=1, column=2)
    else:
        ai()


def create_board():
    global buttons
    global board
    buttons = []
    board = []
    symbol_size = int(root.winfo_width() // 6)
    for i in range(3):
        row = []
        board_row = []
        for j in range(3):
            button = Button(root, font=('bold', symbol_size), width=10, height=10, command=lambda i=i, j=j: user_move(i, j))
            button.grid(row=i, column=j, sticky='nsew')
            row.append(button)
            board_row.append('')
        buttons.append(row)
        board.append(board_row)


def game(button):
    global first_player
    global user_symbol
    global ai_symbol
    if button['text'] == 'X':
        first_player = True
        user_symbol = 'X'
        ai_symbol = 'O'
    else:
        first_player = False
        user_symbol = 'O'
        ai_symbol = 'X'
    clear_root()
    create_board()
    if not first_player:
        ai()


def main():
    text = Label(root, text='Choose a player!', font=('bold', main_font_size))
    text.grid(row=0, column=1, sticky='s')

    btn_x = Button(root, text='X', font=('bold', main_btn_size), command=lambda: game(btn_x))
    btn_x.grid(row=1, column=1)

    btn_o = Button(root, text='O', font=('bold', main_btn_size), command=lambda: game(btn_o))
    btn_o.grid(row=2, column=1, sticky='n')

    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    root.title('Tic Tac Toe')

    root_width = 600
    root_height = 600
    root.geometry(f"{root_width}x{root_height}")

    # Calculate the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position for the main window to center it on the screen
    x = (screen_width - root_width) // 2
    y = (screen_height - root_height) // 2

    # Set the main window's position
    root.geometry(f"+{x}+{y}")

    # Set the number of rows and columns
    for i in range(3):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)

    main_font_size = int(root.winfo_screenwidth() // 30)
    main_btn_size = int(root.winfo_screenwidth() // 30)

    main()
