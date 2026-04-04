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


class MineSweeper:
    """Головний клас застосунку Сапер"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Сапер"
        self.page.padding = 10
        self.page.scroll = ft.ScrollMode.AUTO

        self.level = 0
        self.board_size, self.mines_count = LEVELS[self.level]

        self.cells: list[list[Cell]] = []
        self.cell_cointainers: list[list[ft.Container]] = []

        self._build_ui()
        self.reset()

    def reset(self):
        """Скидання гри та створення нового поля"""
        self.board_size, self.mines_count = LEVELS[self.level]

        self._build_grid()
        self._set_mines()
        self._calc_mines_around()

        self.page.update()

    def _build_ui(self):
        """Створення інтерфейсу"""
        self.grid_column = ft.Column(
            spacing = 1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER 
        )
        self.page.add(self.grid_column)

    def _build_grid(self):
        """Побудова ігрового поля"""
        self.cells = []
        self.cell_cointainers = []
        self.grid_column.controls.clear()

        for x in range(self.board_size):
            row_cells = []
            row_containers = []
            row = ft.Row(spacing = 1, alignment=ft.MainAxisAlignment.CENTER)

            for y in range(self.board_size):
                cell = Cell(x, y)
                row_cells.append(cell)

                cointainer = ft.Container(
                    width = CELL_SIZE,
                    height = CELL_SIZE,
                    bgcolor = ft.Colors.BLUE_GREY_300,
                    border_radius = 2,
                    border = ft.border.all(1, ft.Colors.BLUE_GREY_500),
                    alignment=ft.Alignment.CENTER

                )

                row_containers.append(cointainer)
                row.controls.append(cointainer)

            self.cells.append(row_cells)
            self.cell_cointainers.append(row_containers)
            self.grid_column.controls.append(row)

    def _get_all_cells(self):
        """Генератор для отримання всіх клітинок"""
        for x in range(self.board_size):
            for y in range(self.board_size):
                yield x, y, self.cells[x][y]
    
    def _get_neighbors(self, x: int, y: int):
        """Отримує список сусідніх клітинок (до 8 штук)"""
        result = []
        for xi in range(max(0, x-1), min(x+2, self.board_size)):
            for yi in range(max(0, y-1), min(y+2, self.board_size)):
                if xi != x or yi != y:
                    result.append((xi, yi, self.cells[xi][yi]))
        return result

    def _set_mines(self):
        """Випадкове розміщення мін на полі"""
        position = set()
        while len(position) < self.mines_count:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if (x, y) not in position:
                self.cells[x][y].is_mine = True
                self.cell_cointainers[x][y].content = ft.Text("💣")
                position.add((x, y))
                
    
    def _calc_mines_around(self):
        """Обчислення кількості мін навколо кожної клітинки"""
        for x, y, cell in self._get_all_cells():
            if not cell.is_mine:
                cell.mines_around = sum(
                    1 for _, _, c in self._get_neighbors(x, y) if c.is_mine
                )
                self.cell_cointainers[x][y].content = ft.Text(str(cell.mines_around))

def main(page: ft.Page):
    MineSweeper(page)

ft.run(main)