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
			self.get_scores(no_zeros)
		

	def get_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        
        """        
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		#num of consecutive symbols needed to win
		check_point = 3 if terminal else 2 #if terminal????????
		
		#Check for horizontal lines
		for i in range(rows):
			#Row counts
			rowc_X = 0
			rowc_O = 0
			#Col counts
			colc_X = 0
			colc_O = 0
			# 2 = naught, 1 = cross.
			for j in range(cols):
				return
				#check to see if states[i][j] are crosses or naught. do count stuff 
			
		#Check for vertical lines

		#Check for diagonal lines
	    

	def get_negamax_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2
	    

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
		new_board_state[x,y] = 1 if self.turn_O else -1
		return GameStatus(new_board_state, not self.turn_O)
