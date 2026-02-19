"""
Module de gestion du plateau de jeu Tic-Tac-Toe
Responsable: INES 
"""

import numpy as np
from typing import Tuple, List, Optional


class Board:
    """
    Classe représentant le plateau de jeu 3x3.
    Gère l'état du plateau et les opérations de base.
    """
    
    def __init__(self):
        """Initialise un plateau vide 3x3"""
        self.grid = np.zeros((3, 3), dtype=int)
        # Convention: 0 = vide, 1 = joueur X, -1 = joueur O
        self.current_player = 1  # X commence
        
    def reset(self) -> np.ndarray:
        """
        Réinitialise le plateau à l'état initial.
        
        Returns:
            np.ndarray: Le plateau vide
        """
        self.grid = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        return self.grid.copy()
    
    def get_state(self) -> np.ndarray:
        """
        Retourne l'état actuel du plateau.
        
        Returns:
            np.ndarray: Copie de la grille actuelle
        """
        return self.grid.copy()
    
    def get_available_actions(self) -> List[Tuple[int, int]]:
        """
        Retourne la liste des coups valides (cases vides).
        
        Returns:
            List[Tuple[int, int]]: Liste des positions (row, col) disponibles
        """
        return [(i, j) for i in range(3) for j in range(3) if self.grid[i, j] == 0]
    
    def is_valid_action(self, row: int, col: int) -> bool:
        """
        Vérifie si un coup est valide.
        
        Args:
            row: Ligne (0-2)
            col: Colonne (0-2)
            
        Returns:
            bool: True si le coup est valide
        """
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        return self.grid[row, col] == 0
    
    def make_move(self, row: int, col: int, player: Optional[int] = None) -> bool:
        """
        Effectue un coup sur le plateau.
        
        Args:
            row: Ligne (0-2)
            col: Colonne (0-2)
            player: Joueur (1 ou -1), utilise current_player si None
            
        Returns:
            bool: True si le coup a été effectué, False sinon
        """
        if not self.is_valid_action(row, col):
            return False
        
        if player is None:
            player = self.current_player
            
        self.grid[row, col] = player
        self.current_player = -self.current_player  # Change de joueur
        return True
    
    def __str__(self) -> str:
        """
        Représentation en chaîne du plateau pour debug/console.
        
        Returns:
            str: Affichage formaté du plateau
        """
        symbols = {0: '.', 1: 'X', -1: 'O'}
        lines = []
        lines.append("  0 1 2")
        for i, row in enumerate(self.grid):
            row_str = f"{i} " + " ".join(symbols[cell] for cell in row)
            lines.append(row_str)
        return "\n".join(lines)
    
    def to_string_simple(self) -> str:
        """
        Version compacte pour affichage.
        
        Returns:
            str: Représentation simple du plateau
        """
        symbols = {0: '.', 1: 'X', -1: 'O'}
        return '\n'.join(''.join(symbols[cell] for cell in row) for row in self.grid)
