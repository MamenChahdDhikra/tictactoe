"""
Module principal de l'environnement Tic-Tac-Toe
Responsable: INES

donc ce code combine board.py et rules.py pour créer un environnement complet
"""

import numpy as np
from typing import Tuple, List, Optional, Dict
from board import Board
from rules import RulesChecker


class TicTacToeEnvironment:
    """
    Environnement complet du jeu Tic-Tac-Toe.
    
    Interface standardisée pour que l'IA et l'UI puissent interagir facilement.
    Inspiré des environnements Gym pour compatibilité avec le RL.
    """
    
    def __init__(self):
        """Initialise l'environnement de jeu."""
        self.board = Board()
        self.rules = RulesChecker()
        self.move_history = []
        self.game_count = 0
        
    def reset(self) -> np.ndarray:
        """
        Réinitialise l'environnement pour une nouvelle partie.
        
        Returns:
            np.ndarray: État initial du plateau
        """
        self.board.reset()
        self.move_history = []
        self.game_count += 1
        return self.get_state()
    
    def get_state(self) -> np.ndarray:
        """
        Retourne l'état actuel du jeu.
        
        Returns:
            np.ndarray: Grille 3x3 représentant l'état
        """
        return self.board.get_state()
    
    def get_state_flat(self) -> np.ndarray:
        """
        Retourne l'état sous forme de vecteur 1D (utile pour l'IA).
        
        Returns:
            np.ndarray: Vecteur de 9 éléments
        """
        return self.board.get_state().flatten()
    
    def get_available_actions(self) -> List[Tuple[int, int]]:
        """
        Retourne les actions possibles.
        
        Returns:
            List[Tuple[int, int]]: Liste des positions (row, col) disponibles
        """
        return self.board.get_available_actions()
    
    def get_available_actions_flat(self) -> List[int]:
        """
        Retourne les actions sous forme d'indices 0-8 (utile pour l'IA).
        
        Returns:
            List[int]: Liste des indices disponibles
        """
        return [row * 3 + col for row, col in self.get_available_actions()]
    
    def step(self, action: Tuple[int, int]) -> Tuple[np.ndarray, float, bool, Dict]:
        """
        Exécute une action dans l'environnement.
        
        Args:
            action: Tuple (row, col) représentant la position
            
        Returns:
            Tuple contenant:
                - state (np.ndarray): Nouvel état
                - reward (float): Récompense pour cette action
                - done (bool): True si le jeu est terminé
                - info (dict): Informations additionnelles
        """
        row, col = action
        
        # Vérifier si l'action est valide
        if not self.board.is_valid_action(row, col):
            return self.get_state(), -10.0, True, {'error': 'invalid_move'}
        
        # Sauvegarder le joueur actuel
        current_player = self.board.current_player
        
        # Effectuer le mouvement
        self.board.make_move(row, col)
        self.move_history.append((row, col, current_player))
        
        # Vérifier le statut du jeu
        status = self.rules.get_game_status(self.board.grid)
        
        # Calculer la récompense
        reward = self._calculate_reward(status, current_player)
        
        # Préparer les informations
        info = {
            'status': status,
            'move_count': len(self.move_history),
            'current_player': self.board.current_player
        }
        
        return self.get_state(), reward, status['is_terminal'], info
    
    def step_flat(self, action_idx: int) -> Tuple[np.ndarray, float, bool, Dict]:
        """
        Version avec action sous forme d'indice 0-8.
        
        Args:
            action_idx: Indice de 0 à 8
            
        Returns:
            Même format que step()
        """
        row = action_idx // 3
        col = action_idx % 3
        return self.step((row, col))
    
    def _calculate_reward(self, status: Dict, player: int) -> float:
        """
        Calcule la récompense pour le joueur actuel.
        
        Args:
            status: Statut du jeu
            player: Joueur qui vient de jouer (1 ou -1)
            
        Returns:
            float: Récompense
        """
        if status['winner'] == player:
            return 1.0  # Victoire
        elif status['winner'] == -player:
            return -1.0  # Défaite
        elif status['is_draw']:
            return 0.0  # Match nul
        else:
            return 0.0  # Jeu en cours
    
    def render(self, mode: str = 'console') -> Optional[str]:
        """
        Affiche l'état actuel du jeu.
        
        Args:
            mode: Mode d'affichage ('console' ou 'simple')
            
        Returns:
            str: Représentation du plateau si mode est spécifié
        """
        if mode == 'console':
            print("\n" + "="*15)
            print(f"  Game #{self.game_count}")
            print("="*15)
            print(self.board)
            status = self.rules.get_game_status(self.board.grid)
            if status['winner']:
                winner_name = 'X' if status['winner'] == 1 else 'O'
                print(f"\n🏆 Winner: {winner_name}")
            elif status['is_draw']:
                print("\n🤝 Draw!")
            print(f"Moves: {len(self.move_history)}")
            print("="*15 + "\n")
            return str(self.board)
        elif mode == 'simple':
            return self.board.to_string_simple()
        else:
            return None
    
    def get_winner(self) -> Optional[int]:
        """
        Retourne le gagnant du jeu actuel.
        
        Returns:
            int: 1 (X), -1 (O), ou None
        """
        return self.rules.check_winner(self.board.grid)
    
    def is_game_over(self) -> bool:
        """
        Vérifie si le jeu est terminé.
        
        Returns:
            bool: True si terminé
        """
        return self.rules.is_terminal(self.board.grid)
    
    def get_game_info(self) -> Dict:
        """
        Retourne toutes les informations sur l'état du jeu.
        
        Returns:
            dict: Informations complètes
        """
        status = self.rules.get_game_status(self.board.grid)
        return {
            'state': self.get_state(),
            'state_flat': self.get_state_flat(),
            'available_actions': self.get_available_actions(),
            'available_actions_flat': self.get_available_actions_flat(),
            'move_history': self.move_history.copy(),
            'move_count': len(self.move_history),
            'current_player': self.board.current_player,
            'game_count': self.game_count,
            **status
        }
