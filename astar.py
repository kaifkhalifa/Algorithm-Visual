import pygame
import math
from queue import PriorityQueue




WIDTH = 500
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Kaif's A Star Algorithm")

#sets the colors

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 225)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#main definitions 
class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

# sets the colors of the blocks
	def is_closed(self):
		return self.color == GREY

	def is_open(self):
		return self.color == WHITE

	def is_barrier(self):
		return self.color == RED

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == ORANGE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = GREY

	def make_open(self):
		self.color = WHITE

	def make_barrier(self):
		self.color = RED

	def make_end(self):
		self.color = ORANGE

	def make_path(self):
		self.color = GREEN

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
# updates the grid so that if they have blocks around them it does not go through
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

# sets the function to get fastest possible route The Manhattan Route.
def fastestroute(point1, point2):
	x1, y1 = point1
	x2, y2 = point2
	return abs(x1 - x2) + abs(y1 - y2)


def path(past, present, draw):
	while present in past:
		present = past[present]
		present.make_path()
		draw()


# makes the grid
def make_grid(rows, width):
	grid = [  ]
	gap = width // rows  
	for i in range(rows):
		grid.append([  ])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid

#draws the grid lines
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

#fills the grid
def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()
# algorithm to DISPLAY the fastest route
def algorithm(draw, grid, start, finish):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = fastestroute(start.get_pos(), finish.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == finish:
			path(came_from, finish, draw)
			finish.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + fastestroute(neighbor.get_pos(), finish.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False
# defining clicking the square
def clicked(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

# how many rows you want
def main(win, width):
	ROWS = 20
	grid = make_grid(ROWS, width)
	start = None
	end = None

# looping through the differnt possiblitities and checking them
	run = True
	while run:
# calls the draw function
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False



#left click
			if pygame.mouse.get_pressed()[0]: 
				pos = pygame.mouse.get_pos()
				row, col = clicked(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()
#right click
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = clicked(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
# clears the grid
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)



#what to talk about in an interview
# imports colors
# manhattan route ( fastest possible routes)
# drawing grids and lines with the use of pygames
# unser imputs for the blocks and have algotrithms to construct path

