import random
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

def create_q_model():
    input_layer = layers.Input(shape=(66,))  # 64 board + 2 move encoding

    x = layers.Dense(256, activation='relu')(input_layer)
    x = layers.Dense(256, activation='relu')(x)
    output = layers.Dense(1)(x)  # Q-value

    model = models.Model(inputs=input_layer, outputs=output)
    model.compile(optimizer=optimizers.Adam(learning_rate=0.001), loss='mse')
    return model


def encode_input(board, from_pos, to_pos):
    return np.array(board + [from_pos, to_pos], dtype=np.float32)


class DQNChessAI:
    def __init__(self, model, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.1, gamma=0.95):
        self.model = model
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.gamma = gamma
        self.memory = deque(maxlen=50000)

    def choose_action(self, board, legal_moves):
        actions = [(f, t) for f in legal_moves for t in legal_moves[f]]
        if not actions:
            return None

        if random.random() < self.epsilon:
            return random.choice(actions)

        q_values = []
        for from_pos, to_pos in actions:
            input_data = encode_input(board, from_pos, to_pos).reshape(1, -1)
            q = self.model.predict(input_data, verbose=0)[0][0]
            q_values.append(q)

        best_index = np.argmax(q_values)
        return actions[best_index]

    def store_experience(self, board, action, reward, next_board, done, next_legal_moves):
        self.memory.append((board, action, reward, next_board, done, next_legal_moves))

    def train_from_memory(self, batch_size=32):
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        x_batch, y_batch = [], []

        for board, (from_pos, to_pos), reward, next_board, done, next_legal_moves in batch:
            input_vec = encode_input(board, from_pos, to_pos)
            target = reward

            if not done and next_legal_moves:
                next_qs = []
                for nf, nt in [(f, t) for f in next_legal_moves for t in next_legal_moves[f]]:
                    next_input = encode_input(next_board, nf, nt).reshape(1, -1)
                    next_q = self.model.predict(next_input, verbose=0)[0][0]
                    next_qs.append(next_q)
                if next_qs:
                    target += self.gamma * max(next_qs)

            x_batch.append(input_vec)
            y_batch.append(target)

        self.model.fit(np.array(x_batch), np.array(y_batch), verbose=0, batch_size=batch_size)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def train_dqn(agent, episodes, get_initial_board, get_legal_moves, make_move, is_game_over, get_reward):
    for episode in range(episodes):
        board = get_initial_board()
        done = False

        while not done:
            legal_moves = get_legal_moves(board)
            action = agent.choose_action(board, legal_moves)
            if action is None:
                break

            from_pos, to_pos = action
            next_board = make_move(board.copy(), from_pos, to_pos)
            reward = get_reward(next_board)
            next_legal_moves = get_legal_moves(next_board)
            done = is_game_over(next_board)

            agent.store_experience(board, action, reward, next_board, done, next_legal_moves)
            agent.train_from_memory()

            board = next_board

        print(f"Episode {episode + 1}/{episodes} complete. Epsilon: {agent.epsilon:.4f}")


def get_initial_board():
    # Example: 64 zeros (empty board, placeholder)
    return [0] * 64

def get_legal_moves(board):
    # Placeholder: just make up legal moves for testing
    return {i: [i+1] for i in range(63)} if sum(board) == 0 else {}

def make_move(board, from_pos, to_pos):
    # Placeholder logic: move piece
    board[to_pos] = board[from_pos]
    board[from_pos] = 0
    return board

def is_game_over(board):
    # End after 1 move for demo
    return sum(board) != 0

def get_reward(board):
    # Dummy reward
    return 1 if is_game_over(board) else 0

# =============================
# Main
# =============================
if __name__ == "__main__":
    model = create_q_model()
    agent = DQNChessAI(model)

    train_dqn(
        agent,
        episodes=100,
        get_initial_board=get_initial_board,
        get_legal_moves=get_legal_moves,
        make_move=make_move,
        is_game_over=is_game_over,
        get_reward=get_reward
    )

    model.save("dqn_chess_model.h5")
    print("Training complete and model saved.")
