from pygame.constants import KEYUP
from game_of_life import *
import pygame
import time

CELL_SIZE = 14
ROWS = 50
COLUMNS = 50
WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE * ROWS
WINDOW = pygame.display.set_mode(size=(WIDTH, HEIGHT), flags=pygame.RESIZABLE)
pygame.RESIZABLE
pygame.display.set_caption('Game Of Life')

board = Grid(COLUMNS, ROWS)
run = True
sim_running = False

def draw_grid(win, grid_columns, grid_rows, size):
    for row in range(grid_rows):
        pygame.draw.line(win, (128, 128, 128), (0, row * size), (grid_columns * size, row * size))
        for column in range(grid_columns):
            pygame.draw.line(win, (128, 128, 128), (column * size, 0), (column * size, grid_rows * size))

def draw_cells(win, grid_columns, grid_rows, size, grid):
    for row in range(grid_rows):
        for column in range(grid_columns):
            pygame.draw.rect(win, grid.get_info(column, row)[1], (column * size, row * size, size, size))

def draw(win, grid_columns, grid_rows, size, grid):
    draw_cells(win, grid_columns, grid_rows, size, grid)
    draw_grid(win, grid_columns, grid_rows, size)
    pygame.display.update()

def get_clicked_pos(pos, size):
    x_pos, y_pos = pos
    row = y_pos // size
    column = x_pos // size

    return row, column

def simulation(win, grid_rows, grid_columns, size, grid):
    while True:
        grid.update()
        draw(win, grid_rows, grid_columns, size, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_c:
                    grid.clear()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

while run:
    draw(WINDOW, ROWS, COLUMNS, CELL_SIZE, board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, column = get_clicked_pos(pos, CELL_SIZE)
            board.make(column, row, 1)
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, column = get_clicked_pos(pos, CELL_SIZE)
            board.make(column, row, 0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulation(WINDOW, ROWS, COLUMNS, CELL_SIZE, board)
            elif event.key == pygame.K_c:
                board.clear()