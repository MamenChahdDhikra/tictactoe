"""
Training Script for Q-Learning Agent
Compatible with TicTacToeEnvironment
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from game import TicTacToeEnvironment
from qlearning_agent import QLearningAgent, RandomAgent


# --------------------------------------------------
# PLAY ONE GAME
# --------------------------------------------------

def play_game(agent1, agent2, env: TicTacToeEnvironment, training=True):
    """
    agent1 plays as X (1)
    agent2 plays as O (-1)

    Returns:
        winner: 1 (agent1), -1 (agent2), 0 (draw)
    """

    state = env.reset()
    done = False

    while not done:

        current_player = env.board.current_player
        current_agent = agent1 if current_player == 1 else agent2

        valid_actions = env.get_available_actions_flat()

        action = current_agent.choose_action(
            state.flatten(),
            valid_actions,
            training=training
        )

        if action is None:
            break

        current_agent.record_move(state.flatten(), action)

        next_state, reward, done, info = env.step_flat(action)

        state = next_state

    # -------- GAME OVER --------

    winner = env.get_winner()

    if training:
        if winner == 1:
            agent1.learn(1)
            agent2.learn(-1)

        elif winner == -1:
            agent1.learn(-1)
            agent2.learn(1)

        else:
            agent1.learn(0)
            agent2.learn(0)

    return 0 if winner is None else winner


# --------------------------------------------------
# TRAIN AGENT
# --------------------------------------------------

def train_agent(episodes=50000,
                save_file="trained_agent.pkl",
                plot_progress=True):

    print("Starting Q-Learning Training...")
    print(f"Episodes: {episodes}")
    print("-" * 50)

    env = TicTacToeEnvironment()

    agent1 = QLearningAgent(player=1, epsilon=0.3)
    agent2 = QLearningAgent(player=-1, epsilon=0.3)

    wins = {1: 0, -1: 0, 0: 0}

    win_rate_history = []
    draw_rate_history = []

    checkpoint_interval = max(1, episodes // 20)

    for episode in tqdm(range(episodes), desc="Training"):

        # Decay exploration
        if episode % 10000 == 0 and episode > 0:
            agent1.epsilon = max(0.05, agent1.epsilon * 0.95)
            agent2.epsilon = max(0.05, agent2.epsilon * 0.95)

        winner = play_game(agent1, agent2, env, training=True)
        wins[winner] += 1

        # ---- Logging ----
        if (episode + 1) % checkpoint_interval == 0:

            total = episode + 1
            win_rate = (wins[1] + wins[-1]) / total
            draw_rate = wins[0] / total

            win_rate_history.append(win_rate)
            draw_rate_history.append(draw_rate)

            print(f"\nEpisode {episode + 1}/{episodes}")
            print(f"  X wins: {wins[1]}")
            print(f"  O wins: {wins[-1]}")
            print(f"  Draws: {wins[0]}")
            print(f"  Epsilon: {agent1.epsilon:.3f}")
            print(f"  States learned: {len(agent1.q_table)}")

    # -------- FINAL STATS --------

    print("\nTraining Complete!")
    print("=" * 50)
    print(f"Total games: {episodes}")
    print(f"X wins: {wins[1]}")
    print(f"O wins: {wins[-1]}")
    print(f"Draws: {wins[0]}")
    print(f"States learned: {len(agent1.q_table)}")

    agent1.save(save_file)

    # -------- PLOT --------

    if plot_progress and len(win_rate_history) > 0:

        plt.figure(figsize=(10, 5))

        plt.plot(win_rate_history, label="Win Rate")
        plt.plot(draw_rate_history, label="Draw Rate")

        plt.xlabel("Checkpoint")
        plt.ylabel("Rate")
        plt.title("Training Progress")
        plt.legend()
        plt.grid()

        plt.savefig("training_progress.png")
        plt.show()

    return agent1


# --------------------------------------------------
# TEST AGAINST RANDOM
# --------------------------------------------------

def test_agent(agent_file="trained_agent.pkl", games=1000):

    print(f"\nTesting agent from {agent_file}...")

    env = TicTacToeEnvironment()

    agent = QLearningAgent(player=1)
    agent.load(agent_file)

    random_agent = RandomAgent()

    wins = {1: 0, -1: 0, 0: 0}

    for _ in tqdm(range(games), desc="Testing"):

        winner = play_game(agent, random_agent, env, training=False)
        wins[winner] += 1

    print("\nTest Results vs Random:")
    print(f"Agent wins: {wins[1]}")
    print(f"Random wins: {wins[-1]}")
    print(f"Draws: {wins[0]}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    trained_agent = train_agent(
        episodes=50000,
        save_file="trained_agent.pkl",
        plot_progress=True
    )

    test_agent("trained_agent.pkl", games=1000)
