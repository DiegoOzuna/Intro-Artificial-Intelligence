from GameStatus_5120 import GameStatus

def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
        newScores = game_state.get_scores(terminal)
        return newScores, None   #return value, no move
        
    if maximizingPlayer:
        maxEval = float('-inf')    #AI tries to find the optimal moves that the player would make, (looking for positives)
        bestMove = None
		
        for move in game_state.get_moves():
            game_state.get_new_state(move)
            eval, _ = minimax(game_state, depth-1, False, alpha, beta)
            game_state.undo_move(move)
            if eval > maxEval:
                maxEval = eval
                bestMove = move
            
            alpha = max(alpha, eval)

            if beta <= alpha:
                  break
            
            return maxEval, bestMove   #return value and best move
    else:
        minEval = float('inf')  #AI tries to find the optimal moves that would lower player score (looking for negatives)
        bestMove = None
        for move in game_state.get_moves():
            game_state.get_new_state(move)
            eval, _ = minimax(game_state, depth-1, True, alpha, beta)   #<--- would grab the value at this state
            game_state.undo_move(move)
            if eval < minEval:
                minEval = eval
                bestMove = move
            beta = min(beta, eval)
            if beta <= alpha:
                 break
        return minEval, bestMove     #return value and best move
    

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
	terminal = game_status.is_terminal()
	if (depth==0) or (terminal):
		scores = game_status.get_negamax_scores(terminal)
		return scores, None
	
	best_move = None
	value = float('-inf')
	#original_status = copy.deepcopy(game_status) #copy original status, so we can undo a move
	#checks possible valid moves
	for move in game_status.get_moves():
		#make a move
		game_status.get_new_state(move)
		print(f"Negamax making move at: {move}")
		#recursively call negamax with inverted values
		new_val, _ = negamax(game_status, depth - 1, -1*turn_multiplier,-1*beta, -1*alpha)
		
		#undo move
		game_status.undo_move(move)
		
		#negate value. represents oponents turn
		new_val *= -1
		#update best value and move.
		if new_val > value:
			value = new_val
			best_move = move
			print(f"Best Value updated: {value}")
			print(f"Best Move updated: {move}")

        #apply alpha-beta pruning
		if alpha >= beta:
			break
		
	return -1 * value * turn_multiplier, best_move
		
    
	"""
    YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
    PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
    YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
    IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
    RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    
    """
	
    #return value, best_move