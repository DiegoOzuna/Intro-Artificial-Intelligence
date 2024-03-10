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
import pygame_gui
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
        self.GRID_SIZE = 3
        self. OFFSET = 5

        self.CIRCLE_COLOR = (255, 0, 0)
        self.CROSS_COLOR = (0, 0, 255)

        #Keeping track of what symbol represents the ai and the player for later functions
        # 0 is circle 1 is cross....
        self.AIsym = 0
        self.Playersym = 1

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET

        #THIS IS USED TO HAVE DATA IN GRID....
        self.cells = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]    #this will be used to communicate data

        self.minimax = True   #if true, then we are using minimax, if false then we are using negamax
        
        self.depth = 4         #default of depth is 4. Choice made is to make sure code can run in other environments
                               #we can have gui change this value. for now, a good guess could be made from looking at 8 total steps
                               #(4 from ai, 4 from human...)
        
        self.playersMode = False        #if mode is false, then its player v ai if its true then its player v player

        # This sets the margin between each cell
        self.MARGIN = 5

        # Initialize pygame
        pygame.init()
        
        
        
        #Initialize pygame_gui manager
        self.manager = pygame_gui.UIManager(size)
        
        #Create button instances for the menu...
        self.button_cross = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 50)),
                                                  text='Cross',
                                                  manager=self.manager)
        self.button_circle = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 20), (100, 50)),
                                                        text='Circle',
                                                        manager=self.manager)
        
        self.currentMode = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 20), (300, 50)),
                                                         text='current mode: player_vs_ai',
                                                         manager=self.manager)
        
        self.ai_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 80), (300, 50)),
                                                         text='AI Type: Minimax',
                                                         manager=self.manager)
        
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((146, 200), (300, 50)),
                                                         text='Start',
                                                         manager=self.manager,)
        
        #Creating text for user to see feedback
        self.showSYMchoice = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((20, 80), (215, 50)),
                                         html_text="Your Current Symbol: X",
                                         manager=self.manager)
        
        self.boardSizeText = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((20, 140), (160, 50)),
                                         html_text="Board Size: ",
                                         manager=self.manager)
        
        # Add a dropdown menu for the user to select the board size
        board_sizes = ['3x3', '4x4', '5x5', '6x6']  # Define the available board sizes
        self.board_size_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=board_sizes,
                                                                    starting_option="3x3",
                                                                    relative_rect=pygame.Rect((150, 140), (160, 50)),
                                                                    manager=self.manager)
        
        
        self.game_started = False
        self.game_reset()

    #THIS SECTION (SURROUNDED BY $) IS ALL ABOUT FUNCTIONS FOR THE BUTTONS....
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    def start_game(self):
        if self.game_started:
            # Reset the game and change the button text to 'Start'
            self.game_reset()
            self.game_started = False
            self.start_button.set_text('Start')
        else:
            # Start the game
            self.game_started = True
            self.game_state = GameStatus(self.cells, self.game_started, self.GRID_SIZE)
            self.start_button.set_text('Stop and Reset')
            self.draw_game()

    def changeAI(self):
        self.minimax = not self.minimax

        #Update the text on the button to reflect the current AI algorithm selection
        if self.minimax:
            self.ai_button.set_text('AI Type: Minimax')
        else:
            self.ai_button.set_text('AI Type: Negamax')

    def symChangeCross(self):
        if self.Playersym != 1: #alternate values of AI and Player
            self.Playersym = 1
            self.AIsym = 0
            self.showSYMchoice.html_text = "Your Current Symbol: X"
            self.showSYMchoice.rebuild() #resets the text
        else:
            print("Already Draws cross")
    
    def symChangeCircle(self):
        if self.Playersym != 0: #alternate values of AI and Player.
            self.Playersym = 0
            self.AIsym = 1
            self.showSYMchoice.html_text = "Your Current Symbol: O"
            self.showSYMchoice.rebuild() #resets the text
        else:
            print("Already Draws Circle")

    def changeGrid(self, textDimension):
        if textDimension == '3x3':
            self.GRID_SIZE = 3
        elif textDimension == '4x4':
            self.GRID_SIZE = 4
        elif textDimension == '5x5':
            self.GRID_SIZE = 5
        elif textDimension == '6x6':
            self.GRID_SIZE = 6
        
        #this must be done here to have board change without expanding out of small window given
        self.WIDTH = self.size[0] / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1] / self.GRID_SIZE - self.OFFSET
        self.game_reset()  # Reset the game with the new board size
    
    #this will let user toggle if they want to play with another player or switch back
    def togglePvP(self):
        if self.playersMode != True:
            self.playersMode = True
            self.currentMode.set_text('current mode: player_vs_player')
        else:
            self.playersMode = False
            self.currentMode.set_text('current mode: player_vs_ai')
        
        self.game_reset() #reset the gameboard for pvp

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    
    #this function is meant to safely exit out the game...
    def cleanup(self):
        self.manager.clear_and_reset
        self.manager = None
        pygame.quit()

    def findStartxy(self):
        #purpose of this function is ot grab the screen and make a smaller window for our grid to be located in
        total_grid_width = self.GRID_SIZE * (self.WIDTH/2 + self.MARGIN)
        total_grid_height = self.GRID_SIZE * (self.HEIGHT/2 + self.MARGIN)

        # Calculate starting x coordinate to center the grid horizontally
        start_x = (self.width - total_grid_width) / 2

        # Calculate starting y coordinate to position the grid at the bottom
        start_y = self.height - total_grid_height - self.MARGIN

        return start_x, start_y

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.WHITE)

        start_x, start_y = self.findStartxy()

        # Calculate the width and height of the grid
        grid_width = self.GRID_SIZE * (self.MARGIN + self.WIDTH/2)
        grid_height = self.GRID_SIZE * (self.MARGIN + self.HEIGHT/2)

        # Draw a black rectangle behind the grid
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(start_x-2, start_y-2, grid_width, grid_height))

        # Draw the grid
        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                color = self.WHITE
                pygame.draw.rect(self.screen,
                                color,
                                [start_x + (self.MARGIN + self.WIDTH/2) * column,
                                start_y + (self.MARGIN + self.HEIGHT/2) * row,
                                self.WIDTH/2,
                                self.HEIGHT/2])

        
        # Update and draw the UI elements
        if self.manager:
            self.manager.update(0)
            self.manager.draw_ui(self.screen)

        pygame.display.update()

    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


    def draw_circle(self, screen, x, y):
        radius = min(self.WIDTH, self.HEIGHT) // 4  # Adjust the value as needed
        pygame.draw.circle(screen, self.CIRCLE_COLOR, (x, y), radius, 5)
        

    def draw_cross(self, screen, x, y):
        size = min(self.WIDTH, self.HEIGHT) // 4  # Adjust the value as needed
        pygame.draw.line(screen, self.CROSS_COLOR, (x - size, y - size), (x + size, y + size), 5)
        pygame.draw.line(screen, self.CROSS_COLOR, (x + size, y - size), (x - size, y + size), 5)

    #this function is meant for us to be able to alternate symbols based off user selection.
    def draw_symbol(self, screen, x, y, mySym):
        if mySym == 0:
            self.draw_circle(screen, x, y)
        else:
            self.draw_cross(screen, x, y)


    def is_game_over(self):

        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
        
        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """
    

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)

    def play_human(self, pos, sym):
        #Retrieve the location of the grid...
        start_x, start_y = self.findStartxy()
        #calculate the size of each cell...
        column = int((pos[0] - start_x) // (self.WIDTH/2 + self.MARGIN))
        row = int((pos[1] - start_y) // (self.HEIGHT/2 + self.MARGIN))
        #######################################################################################################
        ## Ensure that the user clicked position was inside the grid location before doing anything else.... ##
        #######################################################################################################
        if 0 <= column < self.GRID_SIZE and 0 <= row < self.GRID_SIZE:
            center_x = start_x + (column * (self.WIDTH/2 + self.MARGIN)) + self.WIDTH // 4
            center_y = start_y + (row * (self.HEIGHT/2 + self.MARGIN)) + self.HEIGHT // 4

            # Set that location to one
            if self.cells[row][column] != 1 and self.cells[row][column] != 2:                       #check if cell is even open to play...
                self.cells[row][column] = 1                             #user playing will leave value of 1
                self.draw_symbol(self.screen,center_x,center_y,sym) #draw at calculated x and y, pass current Playersym choice                                 #draw in cell user symbol...
                print("Click ", pos, "Grid coordinates: ", row, column)
                self.game_state = self.game_state.get_new_state([row,column])
            else:
                print("This cell has a value!")
                                        
                ###############################
                for row in self.game_state.board_state:
                    for cell in row:
                        print(cell, end=' ')
                    print()
                ###############################
        else:
            print("Your clicking empty space?")    #maybe make this a popup after reading further documentation.


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
        
        self.draw_symbol(self.screen,x,y,self.AIsym) #draw at calculated x and y, pass current AIsym choice
        
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
        start_x, start_y = self.findStartxy()
        screen_x = start_x + (grid_x * (self.WIDTH/2 + self.MARGIN)) + self.WIDTH // 4
        screen_y = start_y + (grid_y * (self.HEIGHT/2 + self.MARGIN)) + self.HEIGHT // 4
        return screen_x, screen_y

    
        
        

    def game_reset(self):
        """ 
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
        #Reset the cells to value 0 
        #Reset the cells to match the new GRID_SIZE
        self.cells = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        #Reinitialize the game state
        self.game_state = GameStatus(self.cells, True, self.GRID_SIZE) if self.game_started else GameStatus(self.cells, False, self.GRID_SIZE)
        #Draw the reset game board
        self.draw_game()
        
        

        pygame.display.update()

    def play_game(self, mode = "player_vs_ai"):
        done = False

        # Create a GameStatus object
        self.game_state = GameStatus(tictactoegame.cells, True, self.GRID_SIZE)  # True if it's O's turn, False if it's X's turn


        while not done:
            # Update and draw the UI elements
            
            for event in pygame.event.get():  # User does something
                
                if self.manager: #keep our UI refreshed for menu
                    self.manager.process_events(event)
                    self.manager.update(0)
                    self.manager.draw_ui(self.screen)

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

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED: #check UI_element drop down menu; based on what is selected, restart game and redraw grid
                        if event.ui_element == self.board_size_dropdown:
                            selected_size = event.text
                            self.changeGrid(selected_size)
                          
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.button_cross:
                            self.symChangeCross()
                        elif event.ui_element == self.button_circle:
                            self.symChangeCircle()
                        elif event.ui_element == self.ai_button:
                            self.changeAI()   #change the ai mode
                        elif event.ui_element == self.start_button:
                            self.start_game() #start the game
                        elif event.ui_element == self.currentMode:
                            self.togglePvP()
                        
            

                if self.game_started:
                    if self.playersMode == False:
                        if self.game_state.turn_O == True:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # User clicks the mouse. Get the position
                                pos = pygame.mouse.get_pos()
                                self.play_human(pos, self.Playersym)
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
                    
                    if self.playersMode == True:
                        if self.game_state.turn_O == True:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # User clicks the mouse. Get the position
                                pos = pygame.mouse.get_pos()
                                self.play_human(pos, self.Playersym)
                        else:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                self.play_human(pos, self.AIsym)

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

        self.cleanup()

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