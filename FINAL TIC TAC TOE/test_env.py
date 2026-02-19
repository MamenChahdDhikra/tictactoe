"""
Script de test et démonstration de l'environnement
Responsable:INES

Ce script démontre toutes les fonctionnalités de l'environnement

"""

import numpy as np
from game import TicTacToeEnvironment


def test_basic_game():
    """Test d'une partie basique jouée manuellement."""
    print("\n" + "="*50)
    print("TEST 1: Partie basique")
    print("="*50)
    
    env = TicTacToeEnvironment()
    env.reset()
    
    # Partie exemple: X gagne
    moves = [
        (0, 0),  # X
        (1, 0),  # O
        (0, 1),  # X
        (1, 1),  # O
        (0, 2),  # X gagne (ligne du haut)
    ]
    
    for i, move in enumerate(moves):
        print(f"\nCoup {i+1}: {move}")
        state, reward, done, info = env.step(move)
        env.render('console')
        
        if done:
            print(f"Récompense: {reward}")
            print(f"Info: {info}")
            break


def test_draw_game():
    """Test d'un match nul."""
    print("\n" + "="*50)
    print("TEST 2: Match nul")
    print("="*50)
    
    env = TicTacToeEnvironment()
    env.reset()
    
    # Séquence qui mène à un match nul
    moves = [
        (0, 0),  # X
        (0, 1),  # O
        (0, 2),  # X
        (1, 1),  # O
        (1, 0),  # X
        (1, 2),  # O
        (2, 1),  # X
        (2, 0),  # O
        (2, 2),  # X - Match nul
    ]
    
    for move in moves:
        state, reward, done, info = env.step(move)
    
    env.render('console')
    print(f"Match nul: {info['status']['is_draw']}")


def test_invalid_move():
    """Test de la gestion des coups invalides."""
    print("\n" + "="*50)
    print("TEST 3: Coup invalide")
    print("="*50)
    
    env = TicTacToeEnvironment()
    env.reset()
    
    # Premier coup valide
    env.step((0, 0))
    env.render('console')
    
    # Essayer de jouer sur la même case (invalide)
    print("Tentative de coup invalide sur (0, 0)...")
    state, reward, done, info = env.step((0, 0))
    print(f"Récompense: {reward}")
    print(f"Info: {info}")


def test_available_actions():
    """Test de la récupération des actions disponibles."""
    print("\n" + "="*50)
    print("TEST 4: Actions disponibles")
    print("="*50)
    
    env = TicTacToeEnvironment()
    env.reset()
    
    print("État initial:")
    print(f"Actions disponibles: {env.get_available_actions()}")
    print(f"Actions (format flat): {env.get_available_actions_flat()}")
    
    # Jouer quelques coups
    env.step((0, 0))
    env.step((1, 1))
    env.step((2, 2))
    
    env.render('console')
    print(f"Actions disponibles après 3 coups: {env.get_available_actions()}")
    print(f"Actions (format flat): {env.get_available_actions_flat()}")


def test_state_representations():
    """Test des différentes représentations de l'état."""
    print("\n" + "="*50)
    print("TEST 5: Représentations de l'état")
    print("="*50)
    
    env = TicTacToeEnvironment()
    env.reset()
    
    env.step((0, 0))  # X
    env.step((1, 1))  # O
    
    print("État 2D (grid):")
    print(env.get_state())
    
    print("\nÉtat 1D (flat):")
    print(env.get_state_flat())
    
    print("\nAffichage console:")
    env.render('console')
    
    print("Affichage simple:")
    print(env.render('simple'))


def test_game_info():
    """Test de la récupération des informations complètes."""
    print("\n" + "="*50)
    print("TEST 6: Informations complètes du jeu")
    print("="*50)
    
    env = TicTacToeEnvironment()
    env.reset()
    
    env.step((0, 0))
    env.step((1, 1))
    
    info = env.get_game_info()
    
    print("Informations du jeu:")
    for key, value in info.items():
        if isinstance(value, np.ndarray):
            print(f"  {key}: array{value.shape}")
        else:
            print(f"  {key}: {value}")








def run_all_tests():
    """Exécute tous les tests."""
    test_basic_game()
    test_draw_game()
    test_invalid_move()
    test_available_actions()
    test_state_representations()
    
    
    
    
    print("\n" + "="*60)
    print("✅ TOUS LES TESTS SONT RÉUSSIS!")
    


if __name__ == "__main__":
    run_all_tests()
