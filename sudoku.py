import pygame
import requests
from copy import deepcopy
import sys

WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5

response = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy')
grid = response.json()['board']
grid_original = deepcopy(grid)


def reset(win, solve=False):
    global grid
    if not solve:
        grid = deepcopy(grid_original)

    win.fill(background_color)
    for i in range(10):
        color = (0, 0, 0) if i % 3 == 0 else (128, 128, 128)
        pygame.draw.line(win, color, (50+50*i, 50),
                         (50+50*i, 500), width=2)
        pygame.draw.line(win, color, (50, 50+50*i),
                         (500,  50+50*i), width=2)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(len(grid)):
        for j in range(len(grid)):
            if 0 < grid[i][j] < 10:
                value = myfont.render(
                    str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, (50+50*j+15, 50+50*i))
    pygame.display.update()


def check_win():
    for row in grid:
        if sum(row) != 45:
            return False

    for col in range(9):
        sum_col = 0
        for num in range(9):
            sum_col += grid[num][col]
        if sum_col != 45:
            return False

    for sub_matrix in range(9):
        sum_sub_matrix = 0
        row_index = (sub_matrix % 3)*3
        col_index = (sub_matrix//3)*3
        for row in range(row_index, row_index+3):
            for col in range(col_index, col_index+3):
                sum_sub_matrix += grid[row][col]
        if sum_sub_matrix != 45:
            return False

    return True


def solve(win):
    global grid
    grid = deepcopy(grid_original)

    def isValid(pos, i, j):
        for row in range(9):
            if grid[i][row] == pos:
                return False
        for col in range(9):
            if grid[col][j] == pos:
                return False
        sub_i, sub_j = (i // 3)*3, (j // 3)*3
        for row in range(3):
            for col in range(3):
                if grid[row+sub_i][col+sub_j] == pos:
                    return False
        return True

    def backtracking(i=0, j=0):
        if i == 9:
            reset(win, True)
            return

        if j == 8:
            ni = i+1
            nj = 0
        else:
            ni = i
            nj = j+1

        if grid[i][j] != 0:
            backtracking(ni, nj)
        else:
            for pos in range(1, 10):
                if isValid(pos, i, j):
                    grid[i][j] = pos
                    backtracking(ni, nj)
                    grid[i][j] = 0

    backtracking()


def highlight(win, i, j):
    pygame.draw.line(win, (255, 0, 0), (53+50*(j-1), 52+50*(i-1)),
                     (53+50*(j-1), 99+50*(i-1)), width=4)
    pygame.draw.line(win, (255, 0, 0), (97+50*(j-1), 52+50*(i-1)),
                     (97+50*(j-1), 99+50*(i-1)), width=4)
    pygame.draw.line(win, (255, 0, 0), (52+50*(j-1), 53+50*(i-1)),
                     (98+50*(j-1),  53+50*(i-1)), width=4)
    pygame.draw.line(win, (255, 0, 0), (52+50*(j-1), 97+50*(i-1)),
                     (98+50*(j-1),  97+50*(i-1)), width=4)
    pygame.display.update()


def clear_highlight(win, i, j):
    pygame.draw.line(win, (255, 255, 255), (53+50*(j-1), 52+50*(i-1)),
                     (53+50*(j-1), 99+50*(i-1)), width=4)
    pygame.draw.line(win, (255, 255, 255), (97+50*(j-1), 52+50*(i-1)),
                     (97+50*(j-1), 99+50*(i-1)), width=4)
    pygame.draw.line(win, (255, 255, 255), (52+50*(j-1), 53+50*(i-1)),
                     (98+50*(j-1),  53+50*(i-1)), width=4)
    pygame.draw.line(win, (255, 255, 255), (52+50*(j-1), 97+50*(i-1)),
                     (98+50*(j-1),  97+50*(i-1)), width=4)
    pygame.display.update()


def insert(win, position):
    i, j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    highlight(win, i, j)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                return
            if event.type == pygame.MOUSEBUTTONUP:
                clear_highlight(win, i, j)
                return
            if event.type == pygame.KEYDOWN:
                if grid_original[i-1][j-1] != 0:
                    return
                if event.key == 48:
                    grid[i-1][j-1] = event.key - 48
                    pygame.draw.rect(
                        win, background_color, (position[0]*50+buffer, position[1]*50+buffer, 50-2*buffer, 50-2*buffer))
                    clear_highlight(win, i, j)
                    pygame.display.update()
                    return
                if 0 < event.key - 48 < 10:
                    pygame.draw.rect(
                        win, background_color, (position[0]*50+buffer, position[1]*50+buffer, 50-2*buffer, 50-2*buffer))
                    value = myfont.render(str(event.key-48), True, (0, 0, 0))
                    win.blit(value, (position[0]*50 + 15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    clear_highlight(win, i, j)
                    pygame.display.update()
                    return

                return


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Sudoku Solver')
    reset(win)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    reset(win)
                if event.key == pygame.K_s:
                    solve(win)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if 50 < pos[0] < 500 and 50 < pos[1] < 500:
                    insert(win, (pos[0]//50, pos[1]//50))


main()
