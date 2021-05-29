class Cell:
    def __init__(self, collumn, row, grid_collumns, grid_rows) -> None:
        self.status = 0
        self.row = row
        self.collumn = collumn
        self.neighbors = []
        self.find_neighbors(grid_collumns, grid_rows)
        self.live_neighbors = 0
        self.next_state = 0
    
    def find_neighbors(self, grid_collumns, grid_rows):
        self.neighbors = []
        for row in range(self.row - 1, self.row + 2):
            if (row >= 0) and (row <= grid_rows - 1):
                for collumn in range(self.collumn - 1, self.collumn + 2):
                    if (collumn >= 0) and (collumn <= grid_collumns - 1):
                        if (row == self.row) and (collumn == self.collumn):
                            continue
                        self.neighbors.append([collumn, row])

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
    def __init__(self, grid_collumns, grid_rows) -> None:
        self.grid_rows = grid_rows
        self.grid_collumns = grid_collumns
        self.grid = []
        self.populate(grid_collumns, grid_rows)
    
    def populate(self, grid_collumns, grid_rows):
        for row in range(grid_rows):
            self.grid.append([])
            for collumn in range(grid_collumns):
                self.grid[row].append(Cell(collumn, row, self.grid_collumns, self.grid_rows))
    
    def grid_size_change(self, new_grid_collumns, new_grid_rows):
        row_change = new_grid_rows - self.grid_rows
        collumn_change = new_grid_collumns - self.grid_collumns
        if row_change > 0:
            for new_row in range(row_change):
                self.grid.append([])
                for collumn in range(self.grid_collumns):
                    self.grid[self.grid_rows + new_row].append(Cell(collumn, (self.grid_rows + new_row), self.grid_collumns, self.grid_rows))
            for collumn in range(self.grid_collumns):
                self.grid[self.grid_rows - 1][collumn].find_neighbors(new_grid_collumns, new_grid_rows)
                self.grid[self.grid_rows][collumn].find_live_neighbors(self.grid)
        elif row_change < 0:
            for deleted_row in range(row_change * -1):
                self.grid.pop()
            for collumn in range(self.grid_collumns):
                self.grid[new_grid_rows - 1][collumn].find_neighbors(new_grid_collumns, new_grid_rows)
                self.grid[new_grid_rows - 1][collumn].find_live_neighbors(self.grid)

        if collumn_change > 0:
            for row in range(new_grid_rows):
                for new_collumn in range(collumn_change):
                    self.grid[row].append(Cell((self.grid_collumns + new_collumn), row, self.grid_collumns, self.grid_rows))
            for row in range(new_grid_rows):
                self.grid[row][self.grid_collumns - 1].find_neighbors(new_grid_collumns, new_grid_rows)
                self.grid[row][self.grid_collumns].find_live_neighbors(self.grid)
        elif collumn_change < 0:
            for row in range(new_grid_rows):
                for deleted_collumn in range(collumn_change * -1):
                    self.grid[row].pop()
            for row in range(new_grid_rows):
                self.grid[row][new_grid_collumns - 1].find_neighbors(new_grid_collumns, new_grid_rows)
                self.grid[row][new_grid_collumns - 1].find_live_neighbors(self.grid)

        self.grid_collumns = new_grid_collumns
        self.grid_rows = new_grid_rows
    
    def make(self, collumn, row, value):
        if (value == 1) or (value == 0):
            if self.grid[row][collumn].status == value:
                return
            else:
                self.toggle(collumn, row)
    
    def safe_make(self, collumn, row, value):
        if (value == 1) or (value == 0):
            if self.grid[row][collumn].status == value:
                return
            else:
                self.safe_toggle(collumn, row)
    
    def toggle(self, collumn, row):
        if self.grid[row][collumn].status == 1:
            self.grid[row][collumn].status = 0
            self.grid[row][collumn].find_next_state()
            for neighbor in self.grid[row][collumn].neighbors:
                self.grid[neighbor[1]][neighbor[0]].live_neighbors -= 1
                self.grid[neighbor[1]][neighbor[0]].find_next_state()
        else:
            self.grid[row][collumn].status = 1
            self.grid[row][collumn].find_next_state()
            for neighbor in self.grid[row][collumn].neighbors:
                self.grid[neighbor[1]][neighbor[0]].live_neighbors += 1
                self.grid[neighbor[1]][neighbor[0]].find_next_state()
    
    def safe_toggle(self, collumn, row):
        if self.grid[row][collumn].status == 1:
            self.grid[row][collumn].status = 0
            self.grid[row][collumn].find_next_state()
            for neighbor in self.grid[row][collumn].neighbors:
                self.grid[neighbor[1]][neighbor[0]].live_neighbors -= 1
        else:
            self.grid[row][collumn].status = 1
            self.grid[row][collumn].find_next_state()
            for neighbor in self.grid[row][collumn].neighbors:
                self.grid[neighbor[1]][neighbor[0]].live_neighbors += 1

    def update(self):
        for row in range(self.grid_rows):
            for collumn in range(self.grid_collumns):
                self.safe_make(collumn, row, (self.grid[row][collumn].next_state))
        for row in range(self.grid_rows):
            for collumn in range(self.grid_collumns):
                self.grid[row][collumn].find_next_state()
        #Make a queue for cells that changed and their neighbors and only find the next state for them
    
    def clear(self):
        for row in range(self.grid_rows):
            for collumn in range(self.grid_collumns):
                self.grid[row][collumn].status = 0
                self.grid[row][collumn].next_state = 0
                self.grid[row][collumn].live_neighbors = 0

    def get_info(self, collumn, row):
        color = (255, 255, 255)
        status = self.grid[row][collumn].status
        if status == 1:
            color = (255, 165, 0)
        return [status, color]

    def __repr__(self) -> str:
        string = ''
        for row in range(self.grid_rows):
            for collumn in range(self.grid_collumns):
                string += str(self.grid[row][collumn].status)
            string += '\n'
        return string
