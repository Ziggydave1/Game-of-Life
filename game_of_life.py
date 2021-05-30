class Cell:
    def __init__(self, column, row, grid_columns, grid_rows) -> None:
        self.status = 0
        self.row = row
        self.column = column
        self.neighbors = []
        self.find_neighbors(grid_columns, grid_rows)
        self.live_neighbors = 0
        self.next_state = 0
    
    def find_neighbors(self, grid_columns, grid_rows):
        self.neighbors = []
        for row in range(self.row - 1, self.row + 2):
            if (row >= 0) and (row <= grid_rows - 1):
                for column in range(self.column - 1, self.column + 2):
                    if (column >= 0) and (column <= grid_columns - 1):
                        if (row == self.row) and (column == self.column):
                            continue
                        self.neighbors.append([column, row])

    def find_live_neighbors(self, grid):
        self.live_neighbors = 0
        for neighbor in self.neighbors:
            if grid[neighbor[1]][neighbor[0]].status == 1:
                self.live_neighbors += 1
        self.find_next_state()

    def find_next_state(self):
        if self.live_neighbors == 3:
            self.next_state = 1
        elif self.live_neighbors == 2:
            self.next_state = self.status
        else:
            self.next_state = 0

    def __repr__(self) -> str:
        if self.status == 0:
            return 'a'
        else:
            return 'd'


class Grid:
    def __init__(self, grid_columns, grid_rows) -> None:
        self.grid_rows = grid_rows
        self.grid_columns = grid_columns
        self.grid = []
        self.populate(grid_columns, grid_rows)
    
    def populate(self, grid_columns, grid_rows):
        for row in range(grid_rows):
            self.grid.append([])
            for column in range(grid_columns):
                self.grid[row].append(Cell(column, row, self.grid_columns, self.grid_rows))
    
    def grid_size_change(self, new_grid_columns, new_grid_rows):
        row_change = new_grid_rows - self.grid_rows
        column_change = new_grid_columns - self.grid_columns
        if row_change > 0:
            for new_row in range(row_change):
                self.grid.append([])
                for column in range(self.grid_columns):
                    self.grid[self.grid_rows + new_row].append(Cell(column, (self.grid_rows + new_row), self.grid_columns, self.grid_rows))
            for column in range(self.grid_columns):
                self.grid[self.grid_rows - 1][column].find_neighbors(new_grid_columns, new_grid_rows)
                self.grid[self.grid_rows][column].find_live_neighbors(self.grid)
        elif row_change < 0:
            for deleted_row in range(row_change * -1):
                self.grid.pop()
            for column in range(self.grid_columns):
                self.grid[new_grid_rows - 1][column].find_neighbors(new_grid_columns, new_grid_rows)
                self.grid[new_grid_rows - 1][column].find_live_neighbors(self.grid)

        if column_change > 0:
            for row in range(new_grid_rows):
                for new_column in range(column_change):
                    self.grid[row].append(Cell((self.grid_columns + new_column), row, self.grid_columns, self.grid_rows))
            for row in range(new_grid_rows):
                self.grid[row][self.grid_columns - 1].find_neighbors(new_grid_columns, new_grid_rows)
                self.grid[row][self.grid_columns].find_live_neighbors(self.grid)
        elif column_change < 0:
            for row in range(new_grid_rows):
                for deleted_column in range(column_change * -1):
                    self.grid[row].pop()
            for row in range(new_grid_rows):
                self.grid[row][new_grid_columns - 1].find_neighbors(new_grid_columns, new_grid_rows)
                self.grid[row][new_grid_columns - 1].find_live_neighbors(self.grid)

        self.grid_columns = new_grid_columns
        self.grid_rows = new_grid_rows
    
    def make(self, column, row, value):
        if (value == 1) or (value == 0):
            if self.grid[row][column].status == value:
                return
            else:
                self.toggle(column, row)
    
    def safe_make(self, column, row, value):
        if (value == 1) or (value == 0):
            if self.grid[row][column].status == value:
                return
            else:
                self.safe_toggle(column, row)
    
    def toggle(self, column, row):
        if self.grid[row][column].status == 1:
            self.grid[row][column].status = 0
            self.grid[row][column].find_next_state()
            for neighbor in self.grid[row][column].neighbors:
                self.grid[neighbor[1]][neighbor[0]].live_neighbors -= 1
                self.grid[neighbor[1]][neighbor[0]].find_next_state()
        else:
            self.grid[row][column].status = 1
            self.grid[row][column].find_next_state()
            for neighbor in self.grid[row][column].neighbors:
                self.grid[neighbor[1]][neighbor[0]].live_neighbors += 1
                self.grid[neighbor[1]][neighbor[0]].find_next_state()
    
    def safe_toggle(self, column, row):
        if self.grid[row][column].status == 1:
            self.grid[row][column].status = 0
            self.grid[row][column].find_next_state()
            for neighbor in self.grid[row][column].neighbors:
                self.grid[neighbor[1]][neighbor[0]].live_neighbors -= 1
        else:
            self.grid[row][column].status = 1
            self.grid[row][column].find_next_state()
            for neighbor in self.grid[row][column].neighbors:
                self.grid[neighbor[1]][neighbor[0]].live_neighbors += 1

    def update(self):
        for row in range(self.grid_rows):
            for column in range(self.grid_columns):
                self.safe_make(column, row, (self.grid[row][column].next_state))
        for row in range(self.grid_rows):
            for column in range(self.grid_columns):
                self.grid[row][column].find_next_state()
        #Make a queue for cells that changed and their neighbors and only find the next state for them
    
    def clear(self):
        for row in range(self.grid_rows):
            for column in range(self.grid_columns):
                self.grid[row][column].status = 0
                self.grid[row][column].next_state = 0
                self.grid[row][column].live_neighbors = 0

    def get_info(self, column, row):
        color = (255, 255, 255)
        status = self.grid[row][column].status
        if status == 1:
            color = (255, 165, 0)
        return [status, color]

    def __repr__(self) -> str:
        string = ''
        for row in range(self.grid_rows):
            for column in range(self.grid_columns):
                string += str(self.grid[row][column].status)
            string += '\n'
        return string
