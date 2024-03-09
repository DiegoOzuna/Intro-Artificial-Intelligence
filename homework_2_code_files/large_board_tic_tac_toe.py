"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai" # default mode for playing the game (player vs AI)

class RandomBoardTicTacToe:
    def __init__(self, size = (600, 600)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Grid Size
        self.GRID_SIZE = 4
        self. OFFSET = 5

        self.CIRCLE_COLOR = (255, 0, 0)
        self.CROSS_COLOR = (0, 0, 255)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET

        #THIS IS USED TO HAVE DATA IN GRID....
        self.cells = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]    #this will be used to communicate data

        self.minimax = True   #if true, then we are using minimax, if false then we are using negamax
        
        self.depth = 4         #default of depth is 4. Choice made is to make sure code can run in other environments
                               #we can have gui change this value. for now, a good guess could be made from looking at 8 total steps
                               #(4 from ai, 4 from human...)

        # This sets the margin between each cell
        self.MARGIN = 5

        # Initialize pygame
        pygame.init()
        self.game_reset()

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.BLACK)

        # Draw the grid
        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                color = self.WHITE
                pygame.draw.rect(self.screen,
                                color,
                                [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                self.WIDTH,
                                self.HEIGHT])

        
        """
        YOUR CODE HERE TO DRAW THE GRID OTHER CONTROLS AS PART OF THE GUI
        """
        
        pygame.display.update()

    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


    def draw_circle(self, screen, x, y):
        pygame.draw.circle(screen, self.CIRCLE_COLOR, (x, y), 50, 5)
        

    def draw_cross(self, screen, x, y):
        size = 50
        pygame.draw.line(screen, self.CROSS_COLOR, (x - size, y - size), (x + size, y + size), 5)
        pygame.draw.line(screen, self.CROSS_COLOR, (x + size, y - size), (x - size, y + size), 5)
        

    def is_game_over(self):

        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
        
        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """
    

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)


    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)
        
        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """
        #self.change_turn()
        #pygame.display.update()

        #if minimax is selected
        if(self.minimax):
            #minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):terminal = game_state.is_terminal())
            #NOTE: we only pass the gameboard, the depth assigned, and the current turn. The alpha and beta is handled in function...
            score, bestmove = minimax(self.game_state, self.depth, self.game_state.turn_O)
        #if negamax is selected
        else:
            #negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
            #NOTE: we only pass the gameboard, the depth assigned, and the current turn. The alpha and beta is handled in function...
            score, bestmove = negamax(self.game_state, self.depth, 1)
        
        #update the game state with the best move ai chose...
        #NOTE: move also changes current turn...
        self.move(bestmove)
        #Draw AI move at {bestmove} 
        x, y = self.grid_to_screen(bestmove[1],bestmove[0]) #function translates grid coordinates to screen
        
        self.draw_circle(self.screen,x,y) #draw at calculated x and y
        
        #update display
        pygame.display.update()
       
        terminal = self.game_state.is_terminal()
        if terminal:
            #compute and display final scores
            scores = self.game_state.get_scores(terminal)
            print(f"Final Scores: {scores}") 
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """
        
    def grid_to_screen(self, grid_x, grid_y):
        # Translate grid coordinates to screen coordinates
        screen_x = (grid_x * (self.WIDTH + self.MARGIN)) + self.WIDTH // 2
        screen_y = (grid_y * (self.HEIGHT + self.MARGIN)) + self.HEIGHT // 2
        return screen_x, screen_y
    
        
        

    def game_reset(self):
        self.draw_game()
        """ 
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
        #Reset the cells to value 0 
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                self.cells[row][col] = 0
        
        

        pygame.display.update()

    def play_game(self, mode = "player_vs_ai"):
        done = False

        clock = pygame.time.Clock()

        # Create a GameStatus object
        self.game_state = GameStatus(tictactoegame.cells, True, self.GRID_SIZE)  # True if it's O's turn, False if it's X's turn


        while not done:
            
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                
                """
                YOUR CODE HERE TO HANDLE THE SITUATION IF THE GAME IS OVER. IF THE GAME IS OVER THEN DISPLAY THE SCORE,
                THE WINNER, AND POSSIBLY WAIT FOR THE USER TO CLEAR THE BOARD AND START THE GAME AGAIN (OR CLICK EXIT)
                """
                    
                """
                YOUR CODE HERE TO NOW CHECK WHAT TO DO IF THE GAME IS NOT OVER AND THE USER SELECTED A NON EMPTY CELL
                IF CLICKED A NON EMPTY CELL, THEN GET THE X,Y POSITION, SET ITS VALUE TO 1 (SELECTED BY HUMAN PLAYER),
                DRAW CROSS (OR NOUGHT DEPENDING ON WHICH SYMBOL YOU CHOSE FOR YOURSELF FROM THE gui) AND CALL YOUR 
                PLAY_AI FUNCTION TO LET THE AGENT PLAY AGAINST YOU
                """
                if self.game_state.turn_O == True:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                            # User clicks the mouse. Get the position
                            pos = pygame.mouse.get_pos()
                            # Change the x/y screen coordinates to grid coordinates
                            column = int(pos[0] // (self.WIDTH + self.MARGIN))
                            row = int(pos[1] // (self.HEIGHT + self.MARGIN))
                            # Calculate the center position of the cell
                            center_x = (column * (self.WIDTH + self.MARGIN)) + self.WIDTH // 2
                            center_y = (row * (self.HEIGHT + self.MARGIN)) + self.HEIGHT // 2

                            # Set that location to one
                            if self.cells[row][column] != 1 and self.cells[row][column] != 2:                       #check if cell is even open to play...
                                self.cells[row][column] = 1                             #user playing will leave value of 1
                                self.draw_cross(self.screen, center_x, center_y)                                 #draw in cell user symbol...
                                print("Click ", pos, "Grid coordinates: ", row, column)
                                self.game_state = self.game_state.get_new_state([row,column])
                                

                                ###############################
                                for row in self.game_state.board_state:
                                    for cell in row:
                                        print(cell, end=' ')
                                    print()
                                ###############################

                            else:
                                print("This cell already has a value !")    #maybe make this a popup after reading further documentation.
                else:   
                    #AI TURN !!!!!!!!!!!!!
                    self.play_ai()
                    ###############################
                    print("AI Just busted a move!!")
                    for row in self.cells:
                        for cell in row:
                            print(cell, end=' ')
                        print()
                    ###############################

                if(self.game_state.is_terminal()):
                    done = True
                    
                
                # if event.type == pygame.MOUSEBUTTONUP:
                    # Get the position
                    
                    # Change the x/y screen coordinates to grid coordinates
                    
                    # Check if the game is human vs human or human vs AI player from the GUI. 
                    # If it is human vs human then your opponent should have the value of the selected cell set to -1
                    # Then draw the symbol for your opponent in the selected cell
                    # Within this code portion, continue checking if the game has ended by using is_terminal function
                    
            # Update the screen with what was drawn.
            pygame.display.update()

        pygame.quit()

tictactoegame = RandomBoardTicTacToe()

tictactoegame.play_game()
tictactoegame.draw_game()
"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""



"""
        WILL BE REPURPOSED FOR HUMAN vs HUMAN 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                            # User clicks the mouse. Get the position
                            pos = pygame.mouse.get_pos()
                            # Change the x/y screen coordinates to grid coordinates
                            column = int(pos[0] // (self.WIDTH + self.MARGIN))
                            row = int(pos[1] // (self.HEIGHT + self.MARGIN))
                            # Calculate the center position of the cell
                            center_x = (column * (self.WIDTH + self.MARGIN)) + self.WIDTH // 2
                            center_y = (row * (self.HEIGHT + self.MARGIN)) + self.HEIGHT // 2

                            # Set that location to one
                            if self.cells[row][column] != 1 and self.cells[row][column] != 2:                       #check if cell is even open to play...
                                self.cells[row][column] = 2                             #user playing will leave value of 2
                                self.draw_circle(self.screen, center_x, center_y)                                 #draw in cell user symbol...
                                print("Click ", pos, "Grid coordinates: ", row, column)

                                self.change_turn()
                                ###############################
                                for row in self.cells:
                                    for cell in row:
                                        print(cell, end=' ')
                                    print()
                                ###############################
                            else:
                                print("This cell already has a value !")    #maybe make this a popup after reading further documentation."""