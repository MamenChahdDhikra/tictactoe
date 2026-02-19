"""
Q-Learning Agent compatible with TicTacToeEnvironment
Works with flat states and actions (0–8)
"""

import numpy as np
import random
import pickle
from typing import Dict, List


class QLearningAgent:
    def __init__(self, player: int,
                 epsilon: float = 0.1,
                 alpha: float = 0.5,
                 gamma: float = 0.9):

        self.player = player  # 1 or -1
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

        # Q-table: state_key -> action_values[9]
        self.q_table: Dict[str, np.ndarray] = {}

        # history for learning
        self.state_history = []
        self.action_history = []

    # ---------- STATE HANDLING ----------

    def state_to_key(self, state: np.ndarray) -> str:
        """Convert state array to string key"""
        return state.astype(int).tobytes()

    def get_q_values(self, state_key: str) -> np.ndarray:
        """Return Q-values for state (initialize if new)"""
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(9)
        return self.q_table[state_key]

    # ---------- ACTION SELECTION ----------

    def choose_action(self, state: np.ndarray,
                      valid_actions: List[int],
                      training: bool = True) -> int:

        if not valid_actions:
            return None

        state_key = self.state_to_key(state)
        q_values = self.get_q_values(state_key)

        # --- Exploration ---
        if training and random.random() < self.epsilon:
            return random.choice(valid_actions)

        # --- Exploitation ---
        valid_q = [(a, q_values[a]) for a in valid_actions]
        max_q = max(valid_q, key=lambda x: x[1])[1]

        best_actions = [a for a, q in valid_q if q == max_q]
        return random.choice(best_actions)

    # ---------- LEARNING ----------

    def record_move(self, state: np.ndarray, action: int):
        state_key = self.state_to_key(state)
        self.state_history.append(state_key)
        self.action_history.append(action)

    def learn(self, reward: float):
        """Temporal-difference update backward through episode"""

        target = reward

        for state_key, action in reversed(
                list(zip(self.state_history, self.action_history))):

            q_values = self.get_q_values(state_key)
            current_q = q_values[action]

            # TD update
            new_q = current_q + self.alpha * (target - current_q)
            q_values[action] = new_q

            target = self.gamma * new_q

        self.state_history.clear()
        self.action_history.clear()

    # ---------- SAVE / LOAD ----------

    def save(self, filename: str):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)

    def load(self, filename: str):
        with open(filename, "rb") as f:
            self.q_table = pickle.load(f)

    # ---------- STATS ----------

    def get_stats(self):
        return {
            "states_learned": len(self.q_table),
            "epsilon": self.epsilon,
            "alpha": self.alpha,
            "gamma": self.gamma
        }


class RandomAgent:
    """Opponent agent that plays random valid moves"""

    def choose_action(self, state, valid_actions, training=True):
        return random.choice(valid_actions) if valid_actions else None

    def record_move(self, state, action):
        pass

    def learn(self, reward):
        pass

