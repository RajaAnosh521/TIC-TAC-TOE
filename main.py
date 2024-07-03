import sys
import pygame 
import numpy as np  

pygame.init() 

# Colors
WHITE = (255, 255, 255) 
GRAY = (180, 180, 180)
RED = (255, 0, 0) 
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Proportion & Sizes
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3 
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE AI")
screen.fill(BLACK) 

board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines(color=WHITE):
    """
    Draw the grid lines on the screen.

    Args:
        color (tuple, optional): The color of the lines. Defaults to WHITE.

    Returns:
        None
    """
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures(color=WHITE):
    """
    Draw the figures (circles or crosses) on the screen.

    Args:
        color (tuple, optional): The color of the figures. Defaults to WHITE.

    Returns:
        None
    """
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, 
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, 
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), 
                                 CROSS_WIDTH)
                pygame.draw.line(screen, color, 
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), 
                                 CROSS_WIDTH)

def mark_square(row, col, player):
    """
    Mark a square on the board with a player's symbol.

    Args:
        row (int): The row of the square.
        col (int): The column of the square.
        player (int): The player's symbol (1 or 2).

    Returns:
        None
    """
    board[row][col] = player

def available_square(row, col):
    """
    Check if a square is available (not marked by any player).

    Args:
        row (int): The row of the square.
        col (int): The column of the square.

    Returns:
        bool: True if the square is available, False otherwise.
    """
    return board[row][col] == 0

def is_board_full(check_board=board):
    """
    Check if the board is full (all squares are marked).

    Args:
        check_board (numpy array, optional): The board to check. Defaults to the global board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    """
    Check if a player has won the game.

    Args:
        player (int): The player's symbol (1 or 2).
        check_board (numpy array, optional): The board to check. Defaults to the global board.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True

    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True

    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True

    return False

def minimax(minimax_board, depth, is_maximizing):
    """
    The minimax algorithm for the AI to make the best move.

    Args:
        minimax_board (numpy array): The board to evaluate.
        depth (int): The current depth of the search tree.
        is_maximizing (bool): Whether the AI is maximizing (True) or minimizing (False).

    Returns:
        int: The best score for the AI.
    """
    if check_win(2, minimax_board):
        return 1
    elif check_win(1, minimax_board):
        return -1
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    """
    Find the best move for the AI.

    Returns:
        bool: True if a move was made, False otherwise.
    """
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move!= (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart_game():
    """
    Restart the game by clearing the board and resetting the game state.

    Returns:
        None
    """
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit() 

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE 

                if available_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    if check_win(player):
                        game_over = True
                    player = player % 2 + 1 

                    if not game_over:
                        if best_move():
                            if check_win(2):
                                game_over = True
                            player = player % 2 + 1

                    if not game_over:
                        if is_board_full():
                            game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    game_over = False
                    player = 1

        if not game_over:
            draw_figures()
        else:
            if check_win(1):
                draw_figures(GREEN)
                draw_lines(GREEN)
            elif check_win(2):
                draw_figures(RED)
                draw_lines(RED)
            else:
                draw_figures(GRAY)
                draw_lines(GRAY)

        pygame.display.update()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit() 