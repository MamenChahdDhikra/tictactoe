"""
Tic-Tac-Toe Game Logic
Core board representation and game rules
"""
import numpy as np
from typing import List, Tuple, Optional


class Board:
    """Represents the tic-tac-toe board state"""
    
    def __init__(self):
        self.grid = np.zeros((3, 3), dtype=int)  # 0: empty, 1: X, 2: O
        self.current_player = 1  # X starts
        self.winner = None
        self.move_count = 0
        
    def reset(self):
        """Reset the board to initial state"""
        self.grid = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.winner = None
        self.move_count = 0
        
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Return list of valid (row, col) positions"""
        return [(r, c) for r in range(3) for c in range(3) if self.grid[r, c] == 0]
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move at (row, col) for current player
        Returns True if move was valid, False otherwise
        """
        if self.grid[row, col] != 0 or self.is_game_over():
            return False
        
        self.grid[row, col] = self.current_player
        self.move_count += 1
        
        # Check for winner
        if self._check_winner(self.current_player):
            self.winner = self.current_player
        elif self.move_count == 9:
            self.winner = 0  # Draw
            
        # Switch player
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        
        return True
    
    def is_game_over(self) -> bool:
        """Check if game is finished"""
        return self.winner is not None
    
    def _check_winner(self, player: int) -> bool:
        """Check if specified player has won"""
        # Check rows
        for row in range(3):
            if all(self.grid[row, :] == player):
                return True
        
        # Check columns
        for col in range(3):
            if all(self.grid[:, col] == player):
                return True
        
        # Check diagonals
        if all(self.grid[i, i] == player for i in range(3)):
            return True
        if all(self.grid[i, 2-i] == player for i in range(3)):
            return True
        
        return False
    
    def get_state_key(self) -> str:
        """
        Get unique string representation of board state
        Used as key for Q-table
        """
        return ''.join(str(int(x)) for row in self.grid for x in row)
    
    def clone(self) -> 'Board':
        """Create a copy of this board"""
        new_board = Board()
        new_board.grid = self.grid.copy()
        new_board.current_player = self.current_player
        new_board.winner = self.winner
        new_board.move_count = self.move_count
        return new_board
    
    def get_reward(self, player: int) -> float:
        """
        Get reward from perspective of given player
        +1 for win, -1 for loss, 0 for draw or ongoing
        """
        if self.winner is None:
            return 0.0  # Game not over
        elif self.winner == 0:
            return 0.0  # Draw
        elif self.winner == player:
            return 1.0  # Win
        else:
            return -1.0  # Loss
    
    def __str__(self):
        """String representation for debugging"""
        symbols = {0: '.', 1: 'X', 2: 'O'}
        lines = []
        for row in self.grid:
            lines.append(' '.join(symbols[int(cell)] for cell in row))
        return '\n'.join(lines)
