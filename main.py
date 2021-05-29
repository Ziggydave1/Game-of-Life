from pygame.constants import KEYUP
from game_of_life import *
import pygame
import time

CELL_SIZE = 14
ROWS = 50
COLLUMNS = 50
WIDTH = CELL_SIZE * COLLUMNS
HEIGHT = CELL_SIZE * ROWS
WINDOW = pygame.display.set_mode(size=(WIDTH, HEIGHT), flags=pygame.RESIZABLE)
pygame.RESIZABLE
pygame.display.set_caption('Game Of Life')

board = Grid(COLLUMNS, ROWS)
run = True
sim_running = False

def draw_grid(win, grid_collumns, grid_rows, size):
    for row in range(grid_rows):
        pygame.draw.line(win, (128, 128, 128), (0, row * size), (grid_collumns * size, row * size))
        for collumn in range(grid_collumns):
            pygame.draw.line(win, (128, 128, 128), (collumn * size, 0), (collumn * size, grid_rows * size))

def draw_cells(win, grid_collumns, grid_rows, size, grid):
    for row in range(grid_rows):
        for collumn in range(grid_collumns):
            pygame.draw.rect(win, grid.get_info(collumn, row)[1], (collumn * size, row * size, size, size))

def draw(win, grid_collumns, grid_rows, size, grid):
    draw_cells(win, grid_collumns, grid_rows, size, grid)
    draw_grid(win, grid_collumns, grid_rows, size)
    pygame.display.update()

def get_clicked_pos(pos, size):
    x_pos, y_pos = pos
    row = y_pos // size
    collumn = x_pos // size

    return row, collumn

def simulation(win, grid_rows, grid_collumns, size, grid):
    while True:
        grid.update()
        draw(win, grid_rows, grid_collumns, size, grid)
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
    draw(WINDOW, ROWS, COLLUMNS, CELL_SIZE, board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, collumn = get_clicked_pos(pos, CELL_SIZE)
            board.make(collumn, row, 1)
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, collumn = get_clicked_pos(pos, CELL_SIZE)
            board.make(collumn, row, 0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulation(WINDOW, ROWS, COLLUMNS, CELL_SIZE, board)
            elif event.key == pygame.K_c:
                board.clear()