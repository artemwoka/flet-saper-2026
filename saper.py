import flet as ft
import random
import time

# Рівні складності (розмір поля та кількість мін)
LEVELS = (
    (8,10),  # Легкий: 8x8 поле, 10 мін
    (16,40), # Середній: 16x16 поле, 40 мін
    (24,99), # Важкий: 24x24 поле, 99 мін 
)

# Статус гри
STATUS_READY = 0
STATUS_PLAY = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3

CELL_SIZE = 30


class Cell:
    """Стан однієї клітинки на полі"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.reset()

    def reset(self):
        self.is_mine = False
        self.is_opened = False
        self.is_flagged = False
        self.is_start = False
        self.is_end = False
        self.mines_around = 0

def main(page: ft.Page):
    page.title = "Сапер"
    page.add(ft.Text("Сапер крок 2", size = 30))

ft.run(main)