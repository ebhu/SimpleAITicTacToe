#create board
board = [' ' for _ in range(9)]


def display_board(board):
  """function to display the board"""
  for i in range(3):
    print('|', board[i*3], '|', board[i*3 + 1], '|', board[i*3 + 2], '|')
  print('-' * 11)

def evaluate_board(board, ai_player):
  """function that evaluates if either player has won
  """
  if check_win(board, ai_player):
    return 10
  elif check_win(board, 'X' if ai_player == 'O' else 'O'):
    return -10
  else:
    # Encourage winning moves and discourage losing moves (heuristic)
    empty_cells = [i for i, x in enumerate(board) if x == ' ']
    return 0# Ongoing game

def player_move(board, player):
  """This function handles the human player's move. It keeps prompting the player for a valid move (1-9) until a valid selection is made."""
  while True:
    move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
    if 0 <= move <= 8 and board[move] == ' ':
      board[move] = player
      break
    else:
      print("Invalid move. Try again.")

def check_win(board, player):
  """This function checks if a player has won the game by looking for matching markers in any of the eight winning conditions (rows, columns, diagonals)."""
  win_conditions = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
  for condition in win_conditions:
    if all(board[i] == player for i in condition):
      return True
  return False


def main():
  """The main method for making moves and outputting wins or ties"""
  current_player = 'X'  # Human starts first
  game_over = False
  depth = 2  # Adjust this for AI difficulty (higher depth = more intelligent but slower)
  ai_player = 'O'  # Set AI player to 'O'

  while not game_over:
    display_board(board)

    # Human player's turn
    if current_player == 'X':
      player_move(board, current_player)

    # AI player's turn
    else:
      move = get_ai_move(board, ai_player, depth)
      board[move] = current_player
      print(f"AI Player ({ai_player}) moved to position {move + 1}")  # Positions start from 1 for user

    # Check for winner or tie
    if check_win(board, current_player):
      display_board(board)
      print(f"Player {current_player} wins!")
      game_over = True
    else:
      if all(x != ' ' for x in board):
        print("It's a tie!")
        game_over = True
      current_player = 'O' if current_player == 'X' else 'X'


def minimax(board, depth, ai_player, maximizing_player):
  """This method uses recursion to simulate the outcomes of different
    moves and then backtracks to find the best next move"""

  # Base case: Terminal state or max depth reached
  if depth == 0 or check_win(board, ai_player) or all(x != ' ' for x in board):
    return evaluate_board(board, ai_player)

  if maximizing_player:
    # Find the move with the highest score for the AI
    best_score = -float('inf')
    for i, cell in enumerate(board):
      if cell == ' ':
        board[i] = ai_player
        score = minimax(board, depth - 1, ai_player, False)  # Simulate opponent's move
        board[i] = ' '  # Backtrack
        best_score = max(best_score, score)
    return best_score
  else:
    # Find the move with the lowest score for the human player (maximize for AI)
    best_score = float('inf')
    for i, cell in enumerate(board):
      if cell == ' ':
        board[i] = 'X' if ai_player == 'O' else 'O'  # Simulate human's move
        score = minimax(board, depth - 1, ai_player, True)  # AI's turn next
        board[i] = ' '  # Backtrack
        best_score = min(best_score, score)
    return best_score
  

def get_ai_move(board, ai_player, depth):
  """method to get the best move for the ai"""

  # Initialize best score and best move
  best_score = -float('inf')
  best_move = None

  # Iterate through all empty cells on the board
  for i, cell in enumerate(board):
    if cell == ' ':
      # Simulate AI's move by placing its marker on the empty cell
      board[i] = ai_player
      score = minimax(board, depth - 1, ai_player, False)  # Simulate human's move
      board[i] = ' '  # Backtrack

      # Update best score and best move if this move leads to a better outcome for AI
      if score > best_score:
        best_score = score
        best_move = i
  return best_move  


if __name__ == "__main__":
  main()