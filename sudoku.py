import pygame
import copy
import linecache
import random

#Settings
pygame.font.init()
FONT = pygame.font.SysFont("courier new", 25)
FONT_BOLD = pygame.font.SysFont("consolas", 25, bold = True)
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 480
SQUARE_HEIGHT = WINDOW_HEIGHT/9
SQUARE_WIDTH = WINDOW_WIDTH/9


initial = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

def main():
	#Initializing Game board
	logo = pygame.image.load("sulogo.png")
	pygame.display.set_icon(logo)
	pygame.display.set_caption("Sudoku")
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	screen.fill((255, 255, 255))
	draw_grid_lines(screen)
	#retrieve a puzzle
	clues_and_guesses = get_puzzle(initial)
	game = copy.deepcopy(initial)
	fill_board(initial, screen)
	pygame.display.update()
	#Tile variables
	tileposition = None
	tile = None
	tilecenter = None
	#Logic Flags
	running = True
	clicked = False
	solved = False
	#Game logic
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			#Behavior when mouse clicks on tile
			if event.type == pygame.MOUSEBUTTONDOWN :
				tilesurface = pygame.Surface((SQUARE_WIDTH-3,SQUARE_HEIGHT-3),pygame.SRCALPHA)
				#removes existing highlight if it exists
				if clicked:
					tilesurface.fill((255,255,255))
					screen.blit(tilesurface,tileposition)
					#replaces original digit back after removing highlight
					if game[tile[0]][tile[1]]!=0:
						if initial[tile[0]][tile[1]] != 0:
							text = FONT_BOLD.render(str(game[tile[0]][tile[1]]), 1, (0,0,0)) 
						else:
							text = FONT.render(str(game[tile[0]][tile[1]]), 1, (0,0,0)) 
						screen.blit(text,tilecenter)
				#get current mouse position
				pos = pygame.mouse.get_pos()
				tile = (pos[1]*9//WINDOW_HEIGHT, pos[0]*9//WINDOW_WIDTH) #tile (n,m) 
				tilecenter = ((pos[0]//SQUARE_WIDTH)*SQUARE_WIDTH+(SQUARE_WIDTH/2.5), (pos[1]//SQUARE_HEIGHT)*SQUARE_HEIGHT+SQUARE_HEIGHT/4.5)#for drawing digits
				tileposition = ((pos[0]//SQUARE_WIDTH)*SQUARE_WIDTH+3,(pos[1]//SQUARE_HEIGHT)*SQUARE_HEIGHT+3)#for drawing tiles
				#add highlight to selected tile
				tilesurface.fill((255,255,0,100))
				screen.blit(tilesurface,((pos[0]//SQUARE_WIDTH)*SQUARE_WIDTH+3,(pos[1]//SQUARE_HEIGHT)*SQUARE_HEIGHT+3))
				clicked = True
				pygame.display.update()
			#Key press to Solve game
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and not solved:
				clicked = False
				solve(initial, screen, 30)
				solved = True
				print("You win! press N for a new puzzle")
			#Key press to generate new game
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
				screen.fill((255, 255, 255))
				draw_grid_lines(screen)
				clues_and_guesses = get_puzzle(initial)
				game = copy.deepcopy(initial)
				fill_board(initial, screen)
				pygame.display.update()
				clicked = False
				solved = False
				pygame.display.update()
			#Action once tile is clicked
			elif clicked and event.type == pygame.KEYDOWN:
				ukey = 0
				if event.key == pygame.K_1 or event.key == pygame.K_KP1:
					ukey = 1;
				elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
					ukey = 2;
				elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
					ukey = 3;
				elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
					ukey = 4;
				elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
					ukey = 5;
				elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
					ukey = 6;
				elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
					ukey = 7;
				elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
					ukey = 8;
				elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
					ukey = 9;
				#Behavior if entered key is a digit 
				if ukey in list(range(0,10)):
					#tile is a clue tile
					if initial[tile[0]][tile[1]]!=0:
						pass
					#Erase non clue tile
					elif (event.key == pygame.K_0 or event.key == pygame.K_KP0 or event.key == pygame.K_BACKSPACE):
						#entered key is 0 or backspace
						text = FONT.render("0", 1, (0,0,0))
						textpos = text.get_rect(topleft = tilecenter)
						textsurface = pygame.Surface((textpos.width,textpos.height),pygame.SRCALPHA)
						textsurface.fill((255,255,255))
						screen.blit(textsurface,textpos)
						textsurface.fill((255,255,0,100))
						screen.blit(textsurface,textpos)
						game[tile[0]][tile[1]] = 0
						pygame.display.update(textpos)
						clues_and_guesses -= 1
					#tile is occupied by a guess	
					elif game[tile[0]][tile[1]]!=0 and (game[tile[0]][tile[1]] != ukey):
						#Guess is not valid according to the rules of Sudoku(placeholder)
						if (not is_valid(game, ukey, tile[0], tile[1])):
							pass
						else:
							text = FONT.render(str(ukey), 1, (0,0,0))
							textpos = text.get_rect(topleft = tilecenter)
							textsurface = pygame.Surface((textpos.width,textpos.height),pygame.SRCALPHA)
							textsurface.fill((255,255,255))
							screen.blit(textsurface,textpos)
							textsurface.fill((255,255,0,100))
							screen.blit(textsurface,textpos)
							screen.blit(text,tilecenter)
							game[tile[0]][tile[1]] = ukey
							pygame.display.update(textpos)
							clues_and_guesses += 1
					#tile to be filled is not occupied	
					else:
						#Guess is not valid according to the rules of Sudoku(placeholder)
						if (not is_valid(game, ukey, tile[0], tile[1])):
							pass 
						else:
							text = FONT.render(str(ukey), 1, (0,0,0))
							screen.blit(text, tilecenter)
							game[tile[0]][tile[1]] = ukey
							pygame.display.update(text.get_rect(topleft = tilecenter))
							clues_and_guesses += 1
					#Whole board is filled and valid	
					if clues_and_guesses == 81:
						print("You win! press N for a new puzzle")
				
				
						

#PUZZLE RETRIEVAL
def get_puzzle(game):
	"""generate a new puzzle from the csv file containing 1 million puzzle,
	returns number of clues"""
	filename = "sudoku.csv"
	line = linecache.getline(filename, random.randint(2,1000001))
	clues = 0
	for i in range(81):
		if int(line[i]) != 0:
			clues += 1
		game[i//9][i%9] = int(line[i])
	return clues				

#BOARD CREATION	
def draw_grid_lines(screen):
	#draw the grid lines for the game
	for i in range(1,9):
		if (i %3 ==0):
			pygame.draw.line(screen, (0,0,0), (i*(SQUARE_WIDTH),0), (i*(SQUARE_WIDTH), WINDOW_HEIGHT), 3)
			pygame.draw.line(screen, (0,0,0), (0, i*(SQUARE_HEIGHT)), (WINDOW_WIDTH, i*(SQUARE_HEIGHT)), 3)
		else:
			pygame.draw.line(screen, (0,0,0), (i*(SQUARE_WIDTH),0), (i*(SQUARE_WIDTH), WINDOW_HEIGHT),1)
			pygame.draw.line(screen, (0,0,0), (0, i*(SQUARE_HEIGHT)), (WINDOW_WIDTH, i*(SQUARE_HEIGHT)),1)

def fill_board(board, screen):
	#Fills board with "initial" puzzle
	for row in range(9):
		for col in range(9):
			if board[row][col]!=0:
				text = FONT_BOLD.render(str(board[row][col]), 1, (0,0,0))
				tilecenter = (col*SQUARE_WIDTH+(SQUARE_WIDTH/2.5), (row*SQUARE_HEIGHT+SQUARE_HEIGHT/4.5))
				screen.blit(text,tilecenter)


#SOLVER LOGIC
def is_valid(board, val, row, col):
	#checks if value is valid for currently unoccupied tile
	for i in range(0,9):
		#look for the same value in the same row
		if (board[row][i] == val):
			return False 
		#look for the same value in the same column
		elif(board[i][col] == val):
			return False
	#look for similar value in the same 3x3 square
	for i in range(3):
		for j in range(3):
			i_target = i+3*(row//3)
			j_target = j+3*(col//3)
			if(board[i_target][j_target] == val):
				return False 
	return True

def solve(board, screen, wait):
	#Solves a Sudoku puzzle recursively using backtracking
	for row in range(9):
		for col in range(9):
			#look for the first empty tile and try all possible values
			if(board[row][col] ==0):
				for n in range(1,10):
					if (is_valid(board, n, row, col)):
						text = FONT.render(str(n), 1, (0,0,0))
						tilecenter = (col*SQUARE_WIDTH+(SQUARE_WIDTH/2.5), (row*SQUARE_HEIGHT+SQUARE_HEIGHT/4))
						textpos = text.get_rect(topleft = tilecenter)
						screen.fill((255,255,255),textpos)
						screen.blit(text, tilecenter)
						board[row][col] = n
						pygame.display.update(text.get_rect(topleft = tilecenter))
						pygame.time.wait(wait)
						#recursively call solve() on the next available tile
						if (solve(board, screen, wait)):
							return True
						#erase current tile to restart try all possible values again
						else:
							screen.fill((255,255,255),textpos)
							board[row][col] = 0
							pygame.display.update(text.get_rect(topleft = tilecenter))
							pygame.time.wait(wait)
				#No valid values for current tile	
				return False
	return True
	


	
if __name__ == '__main__':
	main()



		

	


