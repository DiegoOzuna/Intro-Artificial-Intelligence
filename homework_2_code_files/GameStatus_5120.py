# -*- coding: utf-8 -*-
class GameStatus:


	def __init__(self, board_state, turn_O, grid_size):

		self.board_state = board_state
		self.turn_O = turn_O
		self.oldScores = 0
		self.GRID_SIZE = grid_size
		self.winner = ""


	def is_terminal(self):
		"""
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """
		#if board_state has no more 0s, it will return true
		no_zeros = all(0 not in sublist for sublist in self.board_state)

		if no_zeros:
			#Board is full
			scores = self.get_scores(no_zeros)
			print(scores)
			return True
		
		return False #Board is not full
		

	def get_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        
        """        
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = {1: 0, 2: 0, 0: 0}					#keep count of player 1 and 2...
		check_point = 3 if terminal else 2 
		
		# Check rows
		for i in range(rows):
			for j in range(cols - 2):
				if self.board_state[i][j] == self.board_state[i][j+1] == self.board_state[i][j+2]:
					try:
						scores[self.board_state[i][j]] += 1      #update player score if a 3 consecutive pair was found in rows
					except KeyError:
						print(f'Key: {self.board_state[i][j]} does not exist')

		#Check for Cols
		for j in range(cols):
			for i in range(rows - 2):
				if self.board_state[i][j] == self.board_state[i+1][j] == self.board_state[i+2][j]:
					try:
						scores[self.board_state[i][j]] += 1      #update player score if a 3 consecutive pair was found in rows
					except KeyError:
						print(f'Key: {self.board_state[i][j]} does not exist')
	
		#Check for diagonal lines: top left to bottom right
		for i in range(rows-2):
			for j in range(cols -2):
				if self.board_state[i][j] == self.board_state[i+1][j+1] == self.board_state[i+2][j+2]:
					try:
						scores[self.board_state[i][j]] += 1      #update player score if a 3 consecutive pair was found in rows
					except KeyError:
						print(f'Key: {self.board_state[i][j]} does not exist')
		#Diagonal lines: bottom left to top right
		for i in range(2,rows):
			for j in range(cols -2):
				if self.board_state[i][j] == self.board_state[i-1][j+1] == self.board_state[i-2][j+2]:
					try:
						scores[self.board_state[i][j]] += 1      #update player score if a 3 consecutive pair was found in rows
					except KeyError:
						print(f'Key: {self.board_state[i][j]} does not exist')

						
		
		return scores[1] - scores[2]   #return the difference between player and ai (0 is draw, +num is player won, -num is ai won)
	    

	def get_negamax_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = {1: 0, 2: 0, 0: 0}					#keep count of player 1 and 2...
		check_point = 3 if terminal else 2 
		
		# Check rows
		for i in range(rows):
			for j in range(cols - 2):
				if self.board_state[i][j] == self.board_state[i][j+1] == self.board_state[i][j+2]:
					try:
						scores[self.board_state[i][j]] += 100      #update player score if a 3 consecutive pair was found in rows
					except KeyError:
						print(f'Key: {self.board_state[i][j]} does not exist')

		#Check for Cols
		for j in range(cols):
			for i in range(rows - 2):
				if self.board_state[i][j] == self.board_state[i+1][j] == self.board_state[i+2][j]:
					try:
						scores[self.board_state[i][j]] += 100      #update player score if a 3 consecutive pair was found in rows
					except KeyError:
						print(f'Key: {self.board_state[i][j]} does not exist')
	
		#Check for diagonal lines: top left to bottom right
		for i in range(rows-2):
			for j in range(cols -2):
				if self.board_state[i][j] == self.board_state[i+1][j+1] == self.board_state[i+2][j+2]:
					try:
						scores[self.board_state[i][j]] += 100      #update player score if a 3 consecutive pair was found in rows
					except KeyError:
						print(f'Key: {self.board_state[i][j]} does not exist')
		#Diagonal lines: bottom left to top right
		for i in range(2,rows):
			for j in range(cols -2):
				if self.board_state[i][j] == self.board_state[i-1][j+1] == self.board_state[i-2][j+2]:
					try:
						scores[self.board_state[i][j]] += 100      #update player score if a 3 consecutive pair was found in rows
					except KeyError:
						print(f'Key: {self.board_state[i][j]} does not exist')

		
		return -scores[2] + scores[1]   #return the difference between ai and player (0 is draw, +num is player won, -num is ai won)
	    

	def get_moves(self):
		moves = []
		"""
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
		#check cells
		#if cell = 0
		for x in range(self.GRID_SIZE):
			for y in range(self.GRID_SIZE):
				#If a cell is empty
				if self.board_state[x][y] == 0:
					#add it to possible move list
					moves.append((x,y))
		return moves
	
	def get_new_state(self, move):
		new_board_state = self.board_state.copy()
		x, y = move[0], move[1]
		#new_board_state[x,y] = 1 if self.turn_O else -1
		new_board_state[x][y] = 1 if self.turn_O else 2
		return GameStatus(new_board_state, not self.turn_O, self.GRID_SIZE)
	

	def undo_move(self, move):
		
		print("Undo move")
		self.board_state[move[0]][move[1]] = 0
		self.turn_O = not self.turn_O