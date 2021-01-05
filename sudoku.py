import pygame
import copy
import linecache
import random

pygame.font.init()
FONT = pygame.font.SysFont("courier new", 25)
FONT_BOLD = pygame.font.SysFont("consolas", 25, bold = True)
WINDOW_HEIGHT = 360
WINDOW_WIDTH = 360
SQUARE_HEIGHT = WINDOW_HEIGHT//9
SQUARE_WIDTH = WINDOW_WIDTH//9


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
	logo = pygame.image.load("sulogo.png")
	pygame.display.set_icon(logo)
	pygame.display.set_caption("Sudoku")
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	screen.fill((255, 255, 255))
	draw_grid_lines(screen)
	clues_and_guesses = get_puzzle(initial)
	game = copy.deepcopy(initial)
	fill_board(initial, screen)
	pygame.display.update()
	#Logic Flags
	running = True
	clicked = False
	solved = False
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			
			if event.type == pygame.MOUSEBUTTONDOWN :
				pos = pygame.mouse.get_pos()
				tile = (pos[1]*9//WINDOW_HEIGHT, pos[0]*9//WINDOW_WIDTH)
				tilepos = ((pos[0]//SQUARE_WIDTH)*SQUARE_WIDTH+(SQUARE_WIDTH/2.5), (pos[1]//SQUARE_HEIGHT)*SQUARE_HEIGHT+SQUARE_HEIGHT/4.5)
				clicked = True
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and not solved:
				clicked = False
				solve(initial, screen, 30)
				solved = True
				print("You win! press N for a new puzzle")
				
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
				new_game(screen, initial, game, clues_and_guesses)
				clicked = False
				solved = False
				pygame.display.update()
				
			elif clicked and event.type == pygame.KEYDOWN:
				#highlight position tile
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
				if ukey in list(range(0,10)):
					#behavior if entered key is a digit 
					
					if initial[tile[0]][tile[1]]!=0:
						#tile is a clue tile
						pass
					elif (event.key == pygame.K_0 or event.key == pygame.K_KP0 or event.key == pygame.K_BACKSPACE):
						#entered key is 0 or backspace
						text = FONT.render("0", 1, (0,0,0)) 
						textpos = text.get_rect(topleft = tilepos)
						screen.fill((255,255,255),textpos)
						game[tile[0]][tile[1]] = 0
						pygame.display.update(textpos)
						clues_and_guesses -= 1
						
						
					elif game[tile[0]][tile[1]]!=0 and (game[tile[0]][tile[1]] != ukey):
						#tile occupied by guess
						if (not is_valid(game, ukey, tile[0], tile[1])):
							print("INVALID GUESS")
						else:
							text = FONT.render(str(ukey), 1, (0,0,0))
							textpos = text.get_rect(topleft = tilepos)
							screen.fill((255,255,255),textpos)
							screen.blit(text, tilepos)
							game[tile[0]][tile[1]] = ukey
							pygame.display.update(textpos)
							clues_and_guesses += 1
							
					else:
						#new tile to be filled
						if (not is_valid(game, ukey, tile[0], tile[1])):
							print("INVALID GUESS")
						else:
							text = FONT.render(str(ukey), 1, (0,0,0))
							screen.blit(text, tilepos)
							game[tile[0]][tile[1]] = ukey
							pygame.display.update(text.get_rect(topleft = tilepos))
							clues_and_guesses += 1
							
					if clues_and_guesses == 81:
						print("You win! press N for a new puzzle")
				
				
						
				

def new_game(screen, initial, game, clues_and_guesses):
	#updates initial game parameters to create new game
	screen.fill((255, 255, 255))
	draw_grid_lines(screen)
	clues_and_guesses = get_puzzle(initial)
	game = copy.deepcopy(initial)
	fill_board(initial, screen)
	
					
def draw_grid_lines(screen):
	#draw the grid lines for the game
	for i in range(1,9):
		if (i %3 ==0):
			pygame.draw.line(screen, (0,0,0), (i*(WINDOW_WIDTH/9),0), (i*(WINDOW_WIDTH/9), WINDOW_HEIGHT), 3)
			pygame.draw.line(screen, (0,0,0), (0, i*(WINDOW_HEIGHT/9)), (WINDOW_WIDTH, i*(WINDOW_HEIGHT/9)), 3)
		else:
			pygame.draw.line(screen, (0,0,0), (i*(WINDOW_WIDTH/9),0), (i*(WINDOW_WIDTH/9), WINDOW_HEIGHT))
			pygame.draw.line(screen, (0,0,0), (0, i*(WINDOW_HEIGHT/9)), (WINDOW_WIDTH, i*(WINDOW_HEIGHT/9)))

def fill_board(board, screen):
	#Fills board with "initial" puzzle
	for row in range(9):
		for col in range(9):
			if board[row][col]!=0:
				text = FONT_BOLD.render(str(board[row][col]), 1, (0,0,0))
				tilepos = (col*SQUARE_WIDTH+(SQUARE_WIDTH/2.5), (row*SQUARE_HEIGHT+SQUARE_HEIGHT/4))
				screen.blit(text,tilepos)


#PUZZLE RETRIEVALS
def get_puzzle(game):
	#generate a new puzzle from the csv file containing 1 million puzzle
	#returns number of clues
	filename = "sudoku.csv"
	line = linecache.getline(filename, random.randint(2,1000001))
	clues = 0
	for i in range(81):
		if int(line[i]) != 0:
			clues += 1
		game[i//9][i%9] = int(line[i])
	return clues


#SOLVER LOGIC
def is_valid(board, val, row, col):
	#checks if value is valid for currently unoccupied tile
	for i in range(0,9):
		if (board[row][i] == val):
			#look for similar value in same row
			return False 
		elif(board[i][col] == val):
			#look for similar value in same column
			return False
	for i in range(3):
		#look for similar value in same 3x3 square
		for j in range(3):

			i_target = i+3*(row//3)
			j_target = j+3*(col//3)
			if(board[i_target][j_target] == val):
				return False 
	return True

def solve(board, screen, wait):
	for row in range(9):
		for col in range(9):
			if(board[row][col] ==0):
				for n in range(1,10):
					if (is_valid(board, n, row, col)):
						text = FONT.render(str(n), 1, (0,0,0))
						tilepos = (col*SQUARE_WIDTH+(SQUARE_WIDTH/2.5), (row*SQUARE_HEIGHT+SQUARE_HEIGHT/4))
						textpos = text.get_rect(topleft = tilepos)
						screen.fill((255,255,255),textpos)
						screen.blit(text, tilepos)
						board[row][col] = n
						pygame.display.update(text.get_rect(topleft = tilepos))
						pygame.time.wait(wait)
						if (solve(board, screen, wait)):
							return True
						else:
							screen.fill((255,255,255),textpos)
							board[row][col] = 0
							pygame.display.update(text.get_rect(topleft = tilepos))
							pygame.time.wait(wait)
						
				return False
	return True
	


	
if __name__ == '__main__':
	main()



		

	


