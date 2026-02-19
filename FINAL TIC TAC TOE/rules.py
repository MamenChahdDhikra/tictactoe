"""
Module de vérification des règles du Tic-Tac-Toe
Responsable: INES
"""

import numpy as np
from typing import Optional


class RulesChecker:
    """
    Classe pour vérifier les conditions de victoire et de match nul.
    """
    
    @staticmethod
    def check_winner(grid: np.ndarray) -> Optional[int]:
        """
        Vérifie s'il y a un gagnant sur le plateau.
        
        Args:
            grid: Plateau de jeu 3x3
            
        Returns:
            int: 1 si X gagne, -1 si O gagne, None si pas de gagnant
        """
        # Vérifier les lignes
        for row in grid:
            if abs(sum(row)) == 3:
                return int(row[0])
        
        # Vérifier les colonnes
        for col in range(3):
            column_sum = sum(grid[:, col])
            if abs(column_sum) == 3:
                return int(grid[0, col])
        
        # Vérifier diagonale principale (\)
        diag_main = sum([grid[i, i] for i in range(3)])
        if abs(diag_main) == 3:
            return int(grid[0, 0])
        
        # Vérifier diagonale secondaire (/)
        diag_sec = sum([grid[i, 2-i] for i in range(3)])
        if abs(diag_sec) == 3:
            return int(grid[0, 2])
        
        return None
    
    @staticmethod
    def is_draw(grid: np.ndarray) -> bool:
        """
        Vérifie si le jeu est un match nul (plateau plein sans gagnant).
        
        Args:
            grid: Plateau de jeu 3x3
            
        Returns:
            bool: True si match nul
        """
        # Match nul = pas de case vide ET pas de gagnant
        return not np.any(grid == 0) and RulesChecker.check_winner(grid) is None
    
    @staticmethod
    def is_terminal(grid: np.ndarray) -> bool:
        """
        Vérifie si le jeu est terminé (victoire ou match nul).
        
        Args:
            grid: Plateau de jeu 3x3
            
        Returns:
            bool: True si le jeu est terminé
        """
        return RulesChecker.check_winner(grid) is not None or RulesChecker.is_draw(grid)
    
    @staticmethod
    def get_game_status(grid: np.ndarray) -> dict:
        """
        Retourne le statut complet du jeu.
        
        Args:
            grid: Plateau de jeu 3x3
            
        Returns:
            dict: Dictionnaire avec les informations de statut
        """
        winner = RulesChecker.check_winner(grid)
        is_draw = RulesChecker.is_draw(grid)
        is_terminal = winner is not None or is_draw
        
        return {
            'is_terminal': is_terminal,
            'winner': winner,
            'is_draw': is_draw,
            'game_over': is_terminal
        }
