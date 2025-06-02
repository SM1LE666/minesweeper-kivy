class MinesweeperGame:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.first_click = True

    def generate_mines(self, first_click_x, first_click_y):
        import random

        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if (x, y) != (first_click_x, first_click_y) and self.grid[y][x] != -1:
                self.grid[y][x] = -1
                mines_placed += 1
                self.update_adjacent_cells(x, y)

    def update_adjacent_cells(self, mine_x, mine_y):
        for x in range(mine_x - 1, mine_x + 2):
            for y in range(mine_y - 1, mine_y + 2):
                if 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] != -1:
                    self.grid[y][x] += 1

    def reveal_cell(self, x, y):
        if self.first_click:
            self.generate_mines(x, y)
            self.first_click = False

        if self.grid[y][x] == -1:
            return "Game Over"
        elif not self.revealed[y][x]:
            self.revealed[y][x] = True
            if self.grid[y][x] == 0:
                self.reveal_adjacent_cells(x, y)

    def reveal_adjacent_cells(self, x, y):
        for adj_x in range(x - 1, x + 2):
            for adj_y in range(y - 1, y + 2):
                if 0 <= adj_x < self.width and 0 <= adj_y < self.height:
                    self.reveal_cell(adj_x, adj_y)

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True