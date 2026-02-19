
from flask import Flask, request, jsonify
from flask_cors import CORS
from game import TicTacToeEnvironment
from qlearning_agent import QLearningAgent

app = Flask(__name__)
CORS(app)   # ⭐ ADD THIS

env = TicTacToeEnvironment()
agent = QLearningAgent(player=-1)
agent.load("trained_agent.pkl")  # load your trained model

@app.route("/")
def home():
    return "✅ Tic-Tac-Toe AI Server is running!"

@app.route("/reset", methods=["POST"])
def reset():
    state = env.reset()
    return jsonify(state.flatten().tolist())


@app.route("/move", methods=["POST"])
def move():
    try:
        data = request.json
        human_action = int(data["action"])


        # ---- Human move ----
        state, reward, done, info = env.step_flat(human_action)

        if done:
            return jsonify({
                "done": True,
                "winner": env.get_winner(),
                "board": state.flatten().tolist()
            })

        # ---- AI move ----
        valid_actions = env.get_available_actions_flat()

        if not valid_actions:
            return jsonify({
                "done": True,
                "winner": env.get_winner(),
                "board": state.flatten().tolist()
            })

        ai_action = agent.choose_action(
            state.flatten(),
            valid_actions,
            training=False
        )

        state, reward, done, info = env.step_flat(ai_action)

        return jsonify({
            "ai_action": ai_action,
            "done": done,
            "winner": env.get_winner(),
            "board": state.flatten().tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
