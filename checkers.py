#!/usr/bin/env python3
"""
Checkers (Draughts) Game
A classic 8x8 Checkers game with turn-based play, standard capture and kinging rules.
"""

class CheckersGame:
    def __init__(self):
        self.board = self._create_board()
        self.current_player = 'red'  # red goes first
        self.game_over = False
        self.red_pieces = 12
        self.black_pieces = 12

    def _create_board(self):
        """Create an 8x8 board with pieces in starting positions."""
        board = [['.' for _ in range(8)] for _ in range(8)]
        
        for row in range(8):
            for col in range(8):
                # Only play on dark squares (where row+col is odd)
                if (row + col) % 2 == 1:
                    if row < 3:
                        board[row][col] = 'B'  # Black pieces (top)
                    elif row > 4:
                        board[row][col] = 'R'  # Red pieces (bottom)
        
        return board

    def display_board(self):
        """Display the current board state."""
        print("\n  a b c d e f g h")
        for row in range(8):
            print(f"{row + 1} ", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece == '.':
                    print(". ", end="")
                elif piece == 'R':
                    print("R ", end="")
                elif piece == 'r':
                    print("rk", end="")  # Red king
                elif piece == 'B':
                    print("B ", end="")
                elif piece == 'b':
                    print("bk", end="")  # Black king
            print()
        print()

    def get_piece_color(self, piece):
        """Get the color of a piece."""
        if piece in ('R', 'r'):
            return 'red'
        elif piece in ('B', 'b'):
            return 'black'
        return None

    def is_valid_position(self, row, col):
        """Check if a position is on the board."""
        return 0 <= row < 8 and 0 <= col < 8

    def get_valid_moves(self, player):
        """Get all valid moves for a player."""
        moves = []
        captures = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                piece_color = self.get_piece_color(piece)
                
                if piece_color == player:
                    is_king = piece.islower()
                    directions = []
                    
                    if player == 'red' or is_king:
                        directions.append((-1, -1))  # Up-left
                        directions.append((-1, 1))   # Up-right
                    
                    if player == 'black' or is_king:
                        directions.append((1, -1))   # Down-left
                        directions.append((1, 1))    # Down-right
                    
                    for dr, dc in directions:
                        # Check simple move
                        new_row, new_col = row + dr, col + dc
                        if self.is_valid_position(new_row, new_col):
                            if self.board[new_row][new_col] == '.':
                                moves.append({
                                    'from': (row, col),
                                    'to': (new_row, new_col),
                                    'capture': None
                                })
                            
                            # Check capture
                            capture_row, capture_col = row + 2*dr, col + 2*dc
                            if self.is_valid_position(capture_row, capture_col):
                                capture_piece = self.board[new_row][new_col]
                                if (capture_piece != '.' and 
                                    self.get_piece_color(capture_piece) != player and
                                    self.board[capture_row][capture_col] == '.'):
                                    captures.append({
                                        'from': (row, col),
                                        'to': (capture_row, capture_col),
                                        'capture': (new_row, new_col)
                                    })
        
        # Mandatory capture rule: if capture is available, must capture
        return captures if captures else moves

    def parse_move(self, move_str):
        """Parse a move string like 'a3-b4' or 'h6-f8'."""
        try:
            if len(move_str) != 5 or move_str[2] != '-':
                return None, None
            
            from_col = ord(move_str[0].lower()) - ord('a')
            from_row = int(move_str[1]) - 1
            to_col = ord(move_str[3].lower()) - ord('a')
            to_row = int(move_str[4]) - 1
            
            if not (0 <= from_row < 8 and 0 <= from_col < 8 and
                    0 <= to_row < 8 and 0 <= to_col < 8):
                return None, None
            
            return (from_row, from_col), (to_row, to_col)
        except (ValueError, IndexError):
            return None, None

    def execute_move(self, from_pos, to_pos):
        """Execute a move and update the board."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = '.'
        self.board[to_row][to_col] = piece
        
        # Check for capture
        captured_row = (from_row + to_row) // 2
        captured_col = (from_col + to_col) // 2
        if self.board[captured_row][captured_col] != '.':
            captured_piece = self.board[captured_row][captured_col]
            self.board[captured_row][captured_col] = '.'
            color = self.get_piece_color(captured_piece)
            if color == 'red':
                self.red_pieces -= 1
            else:
                self.black_pieces -= 1
        
        # Check for kinging
        if self.current_player == 'red' and to_row == 0 and piece == 'R':
            self.board[to_row][to_col] = 'r'  # Red king
        elif self.current_player == 'black' and to_row == 7 and piece == 'B':
            self.board[to_row][to_col] = 'b'  # Black king

    def check_winner(self):
        """Check if there's a winner."""
        if self.red_pieces == 0:
            return 'black'
        elif self.black_pieces == 0:
            return 'red'
        
        # Check if current player has no valid moves
        moves = self.get_valid_moves(self.current_player)
        if not moves:
            return 'black' if self.current_player == 'red' else 'red'
        
        return None

    def play_game(self):
        """Main game loop."""
        print("=" * 50)
        print("    WELCOME TO CHECKERS!")
        print("=" * 50)
        print("\nHow to play:")
        print("- Enter moves as 'from-to' notation (e.g., a3-b4)")
        print("- Columns: a-h, Rows: 1-8")
        print("- Pieces: R = Red, B = Black, rk = Red King, bk = Black King")
        print("- Captures are mandatory when available")
        print("- First player to eliminate all opponent pieces wins!")
        print()
        
        while not self.game_over:
            self.display_board()
            
            # Get valid moves for current player
            valid_moves = self.get_valid_moves(self.current_player)
            
            if not valid_moves:
                winner = 'black' if self.current_player == 'red' else 'red'
                print(f"\nNo valid moves for {self.current_player}!")
                print(f"{'=' * 50}")
                print(f"    {winner.upper()} WINS!")
                print(f"{'=' * 50}")
                break
            
            print(f"\n{self.current_player.upper()}'s turn")
            print(f"Red pieces remaining: {self.red_pieces}")
            print(f"Black pieces remaining: {self.black_pieces}")
            
            # Display available moves for reference
            if valid_moves:
                print("\nAvailable moves:")
                for i, move in enumerate(valid_moves):
                    from_pos = move['from']
                    to_pos = move['to']
                    from_square = chr(ord('a') + from_pos[1]) + str(from_pos[0] + 1)
                    to_square = chr(ord('a') + to_pos[1]) + str(to_pos[0] + 1)
                    capture = " (CAPTURE!)" if move['capture'] else ""
                    print(f"  {i+1}. {from_square} -> {to_square}{capture}")
            
            # Get player input
            while True:
                try:
                    move_input = input(f"\nEnter your move (e.g., a3-b4): ").strip()
                    
                    if move_input.lower() in ('quit', 'exit', 'q'):
                        print("\nGame cancelled.")
                        return
                    
                    from_pos, to_pos = self.parse_move(move_input)
                    
                    if from_pos is None or to_pos is None:
                        print("Invalid format. Use 'a3-b4' format.")
                        continue
                    
                    # Verify move is valid
                    move_found = False
                    for move in valid_moves:
                        if move['from'] == from_pos and move['to'] == to_pos:
                            move_found = True
                            break
                    
                    if not move_found:
                        print("Invalid move. Try again.")
                        continue
                    
                    # Execute the move
                    self.execute_move(from_pos, to_pos)
                    
                    # Check for winner
                    winner = self.check_winner()
                    if winner:
                        self.display_board()
                        print(f"\n{'=' * 50}")
                        print(f"    {winner.upper()} WINS!")
                        print(f"{'=' * 50}")
                        self.game_over = True
                        break
                    
                    # Switch turns
                    self.current_player = 'black' if self.current_player == 'red' else 'red'
                    break
                    
                except KeyboardInterrupt:
                    print("\n\nGame interrupted.")
                    return


def main():
    """Main entry point."""
    game = CheckersGame()
    game.play_game()
    
    # Ask if players want to restart
    while True:
        play_again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if play_again in ('y', 'yes'):
            game = CheckersGame()
            game.play_game()
        elif play_again in ('n', 'no'):
            print("\nThanks for playing!")
            break
        else:
            print("Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()
