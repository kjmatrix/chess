import pygame
import sys
import os

pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (0, 255, 0)
BOARD_SIZE = 800
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // ROWS

screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Chess - Full Legal Moves with Images")

# Board setup
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

def setup_board():
    order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(COLS):
        board[1][i] = 'white_pawn'
        board[6][i] = 'black_pawn'
        board[0][i] = f'white_{order[i]}'
        board[7][i] = f'black_{order[i]}'

setup_board()

selected = None
valid_moves = []

# Load piece images with your paths
piece_images = {}

def load_images():
    image_paths = {
        'white_pawn':   r"C:\Users\ravir\images\wP.png.png",
        'white_knight': r"C:\Users\ravir\images\wN.png.png",
        'white_bishop': r"C:\Users\ravir\images\wB.png.png",
        'white_rook':   r"C:\Users\ravir\images\wR.png.png",
        'white_queen':  r"C:\Users\ravir\images\wQ.png.png",
        'white_king':   r"C:\Users\ravir\images\wK.png.png",
        'black_pawn':   r"C:\Users\ravir\images\bP.png.png",
        'black_knight': r"C:\Users\ravir\images\bN.png.png",
        'black_bishop': r"C:\Users\ravir\images\bB.png.png",
        'black_rook':   r"C:\Users\ravir\images\bR.png.png",
        'black_queen':  r"C:\Users\ravir\images\bQ.png.png",
        'black_king':   r"C:\Users\ravir\images\bK.png.png",
    }

    for name, path in image_paths.items():
        image = pygame.image.load(path)
        piece_images[name] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

load_images()

# Movement logic
def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def add_moves_in_directions(start_row, start_col, directions, team):
    moves = []
    for dr, dc in directions:
        r, c = start_row + dr, start_col + dc
        while in_bounds(r, c):
            target = board[r][c]
            if target is None:
                moves.append((r, c))
            elif target.startswith(team):
                break
            else:
                moves.append((r, c))
                break
            r += dr
            c += dc
    return moves

def get_valid_moves(piece, row, col):
    moves = []
    team = 'white' if piece.startswith('white') else 'black'
    enemy = 'black' if team == 'white' else 'white'

    if piece.endswith('pawn'):
        direction = 1 if team == 'white' else -1
        start_row = 1 if team == 'white' else 6

        if in_bounds(row + direction, col) and board[row + direction][col] is None:
            moves.append((row + direction, col))
            if row == start_row and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))

        for dx in [-1, 1]:
            r, c = row + direction, col + dx
            if in_bounds(r, c) and board[r][c] and board[r][c].startswith(enemy):
                moves.append((r, c))

    elif piece.endswith('knight'):
        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if in_bounds(r, c):
                target = board[r][c]
                if not target or target.startswith(enemy):
                    moves.append((r, c))

    elif piece.endswith('bishop'):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves += add_moves_in_directions(row, col, directions, team)

    elif piece.endswith('rook'):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        moves += add_moves_in_directions(row, col, directions, team)

    elif piece.endswith('queen'):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        moves += add_moves_in_directions(row, col, directions, team)

    elif piece.endswith('king'):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if in_bounds(r, c):
                target = board[r][c]
                if not target or target.startswith(enemy):
                    moves.append((r, c))

    return moves

# Drawing functions
def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if (row + col) % 2 == 1 else WHITE
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if (row, col) in valid_moves:
                pygame.draw.circle(screen, HIGHLIGHT,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   10)

            piece = board[row][col]
            if piece:
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Main game loop
while True:
    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

            if selected:
                if (row, col) in valid_moves:
                    board[row][col] = board[selected[0]][selected[1]]
                    board[selected[0]][selected[1]] = None
                selected = None
                valid_moves = []
            else:
                piece = board[row][col]
                if piece:
                    selected = (row, col)
                    valid_moves = get_valid_moves(piece, row, col)
