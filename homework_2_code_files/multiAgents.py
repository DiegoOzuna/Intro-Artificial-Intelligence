from GameStatus_5120 import GameStatus

def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    #first we check if game is terminal or depth is 0...
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
        newScores = game_state.get_scores(terminal) #if it is, then grab the scores and return (will propagate back up)
        return newScores, None   #return value, no move
        
    
    if maximizingPlayer:
        bestEval = float('-inf')    #AI tries to find the optimal moves that the player would make, (looking for positives)
        possible_moves = game_state.get_moves()
        for move in possible_moves: #look at each possible move (ie, each position with 0)
           
            new_state = game_state.get_new_state(move) #grab and store that state in m...
            eval, _ = minimax(new_state, depth-1, False, alpha, beta) #run minimax on that gamestate...
            new_state.undo_move(move) #then undo that move done in the gamestate
            if eval > bestEval: #if the eval is better than our max, reassign both the eval and the bestmove...
                print(f"eval > maxEval.. reassigning maxEval, bestMove")
                bestEval = eval
                bestMove = move
            ###############################
            print(f"BestMove, maxEval:  ({bestMove},{bestEval})")
            ################################
            

            #if beta is found to be lower than eval, we prune
            if eval >= beta:
                  break    
            
            #set alpha to the max value
            alpha = max(alpha, eval)
            
    else:
        bestEval = float('inf')  #AI tries to find the optimal moves that would lower player score (looking for negatives)
        possible_moves = game_state.get_moves()
        for move in possible_moves: #look at each possible move (ie, each position with 0)

            new_state = game_state.get_new_state(move) 
            eval, _ = minimax(new_state, depth-1, True, alpha, beta)   #run minimax on that gamestate...
            new_state.undo_move(move) #then undo that move done in the gamestate
            if eval < bestEval: #if the eval is lower than our min, reassign both the eval and the bestmove...
                print(f"eval > minEval.. reassigning minEval, bestMove")
                bestEval = eval
                bestMove = move
            ###############################
            print(f"BestMove, minEval:  ({bestMove},{bestEval})")
            ################################
            
            #if beta is found to be lower than alpha, we prune
            if eval <= alpha:
                 break
            
            beta = min(beta, eval)
    return bestEval, bestMove     #return value and best move






def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    #first we check if game is terminal or depth is 0...
    terminal = game_status.is_terminal()
    if depth == 0 or terminal:
        scores = game_status.get_negamax_scores(terminal) #grab the scores and return (will propagate back up)
        return scores, None
    
    best_move = None
    value = float('-inf')
    
    # checks possible valid moves
    for move in game_status.get_moves():
        # make a move and get new state
        new_state = game_status.get_new_state(move)
        print(f"Negamax making move at: {move}")
        
        # recursively call negamax with inverted values
        new_val, _ = negamax(new_state, depth - 1, -1 * turn_multiplier, -1 * beta, -1 * alpha)
        
        # undo move
        new_state.undo_move(move)
        
        # negate value. represents opponent's turn
        new_val *= -1
        
        # update best value and move
        if new_val > value:
            value = new_val
            best_move = move
            print(f"Best Value updated: {value}")
            print(f"Best Move updated: {move}")
            
        # apply alpha-beta pruning
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    # if best move is found return inverted value, best_move; else return inverted value, game_status.get_moves()[0]
    return (-1 * value * turn_multiplier, best_move) if best_move is not None else (-1 * value * turn_multiplier, game_status.get_moves()[0])

	
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