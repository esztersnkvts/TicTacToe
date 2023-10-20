from tkinter import *


# Define the depth limit for the Minimax algorithm (adjust as needed)
MAX_DEPTH = 5


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

    button_x_new_game = int(window.winfo_width() // 3.2)
    button_y_new_game = int(window.winfo_height() // 2)
    button_x_exit = int(window.winfo_width() // 2.5)
    button_y_exit = int(window.winfo_height() // 1.5)

    new_game_btn = Button(window, text='New Game', font=('bold', 25), command=reset)
    # new_game_btn.place(x=130, y=200)
    # new_game_btn.pack(side=TOP, anchor='center')
    new_game_btn.place(x=button_x_new_game, y=button_y_new_game)

    exit_btn = Button(window, text='Exit', font=('bold', 25), command=exit_game)
    # exit_btn.place(x=170, y=250)
    # exit_btn.pack()
    exit_btn.place(x=button_x_exit, y=button_y_exit)


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
    buttons[ai_row][ai_col].config(text=ai_symbol, font=('bold', 100), anchor="nw", padx=65, pady=40, state='disabled')
    board[ai_row][ai_col] = ai_symbol
    if check_win(board, ai_symbol):
        end_game_window()
        text = Label(window, text='You lost!', font=('bold', 35))
        text_x = int(window.winfo_width() // 3)
        text_y = int(window.winfo_height() // 4)
        # text.place(x=135, y=100)
        text.place(x=text_x, y=text_y)
        disable_all_buttons()
    elif len(get_empty_cells(board)) == 0:
        end_game_window()
        text = Label(window, text='Draw!', font=('bold', 35))
        text.place(x=160, y=100)


def user_move(row, col):
    buttons[row][col].config(text=user_symbol, font=('bold', 100), anchor="nw", padx=65, pady=40, state='disabled')
    board[row][col] = user_symbol
    if check_win(board, user_symbol):
        end_game_window()
        text = Label(window, text='You won!', font=('bold', 35))
        text.place(x=135, y=100)
        disable_all_buttons()
    elif len(get_empty_cells(board)) == 0:
        end_game_window()
        text = Label(window, text='Draw!', font=('bold', 35))
        text.place(x=160, y=100)
    else:
        ai()


def create_board():
    global buttons
    global board
    buttons = []
    board = []
    pos_x = 200
    pos_y = 200
    for i in range(3):
        row = []
        board_row = []
        for j in range(3):
            button = Button(root, width=20, height=20, command=lambda i=i, j=j: user_move(i, j))
            button.place(x=j*pos_x, y=i*pos_y)
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
    text = Label(root, text='Choose a player!', font=('bold', 50))
    text.place(x=125, y=150)

    btn_x = Button(root, text='X', font=('bold', 75), command=lambda: game(btn_x))
    btn_x.place(x=190, y=270)

    btn_o = Button(root, text='O', font=('bold', 75), command=lambda: game(btn_o))
    btn_o.place(x=320, y=270)

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

    main()
