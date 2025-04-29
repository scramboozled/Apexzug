import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random

# 1. Chess Board Representation
def board_to_input(board):
    input_tensor = np.zeros((12, 8, 8), dtype=np.float32)
    
    piece_dict = {
        'wp': 1, 'bp': -1, 'wn': 2, 'bn': -2, 'wb': 3, 'bb': -3,
        'wr': 4, 'br': -4, 'wq': 5, 'bq': -5, 'wk': 6, 'bk': -6
    }

    for i, square in enumerate(board):
        if square in piece_dict:
            piece_value = piece_dict[square]
            channel = piece_value if piece_value > 0 else -piece_value
            row, col = divmod(i, 8)
            input_tensor[channel, row, col] = 1 if piece_value > 0 else -1
    return input_tensor

# 2. Neural Network (CNN) for Policy and Value
class ChessNN(nn.Module):
    def __init__(self):
        super(ChessNN, self).__init__()
        self.conv1 = nn.Conv2d(12, 128, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 1024)
        self.fc_policy = nn.Linear(1024, 64)  # 64 possible moves
        self.fc_value = nn.Linear(1024, 1)    # Win/Draw/Loss prediction

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, 128 * 8 * 8)  # Flatten for fully connected layers
        x = F.relu(self.fc1(x))
        policy = self.fc_policy(x)
        value = torch.tanh(self.fc_value(x))  # Output between -1 and 1
        return policy, value

# 3. Monte Carlo Tree Search (MCTS)
class MCTS:
    def __init__(self, model, simulations=100):
        self.model = model
        self.simulations = simulations
    
    def run(self, board):
        input_tensor = board_to_input(board)
        input_tensor = torch.tensor(input_tensor, dtype=torch.float32).unsqueeze(0)
        
        policy, value = self.model(input_tensor)
        policy = policy.detach().numpy().flatten()
        
        move = np.argmax(policy)  # Choose move with highest probability
        return move, value.item()

# 4. Self-Play for Training
class SelfPlay:
    def __init__(self, model, mcts, episodes=1000):
        self.model = model
        self.mcts = mcts
        self.episodes = episodes

    def self_play_game(self):
        board = [' ' for _ in range(64)]  # Empty board
        game_history = []
        
        for episode in range(self.episodes):
            move, value = self.mcts.run(board)
            game_history.append((board, move, value))
            # Simulate the move on the board (simplified, actual move logic needed)
            board[move] = 'wp'  # Placeholder for actual move logic
        
        return game_history

    def train_model(self, optimizer):
        for episode in range(self.episodes):
            game_history = self.self_play_game()
            for state, move, value in game_history:
                # Update model using value and policy loss
                input_tensor = board_to_input(state)
                input_tensor = torch.tensor(input_tensor, dtype=torch.float32).unsqueeze(0)
                print(move, value, episode)
                output_policy, output_value = self.model(input_tensor)
                
                policy_loss = F.cross_entropy(output_policy, torch.tensor([move]))
                value_loss = F.mse_loss(output_value, torch.tensor([[value]], dtype=torch.float32))
                loss = policy_loss + value_loss
                
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        

# 5. Main Loop for Model Training
def train_alpha_zero():
    # Initialize model and optimizer
    model = ChessNN()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    mcts = MCTS(model, simulations=50)
    self_play = SelfPlay(model, mcts, episodes=1000)

    # Train the model
    print('HI')
    self_play.train_model(optimizer)
    print('Hi')

# 6. Running the Model to Predict Moves
def predict_move(board, model):
    input_tensor = board_to_input(board)
    input_tensor = torch.tensor(input_tensor, dtype=torch.float32).unsqueeze(0)
    
    policy, value = model(input_tensor)
    move = np.argmax(policy.detach().numpy())  # Choose move with highest probability
    return move, value.item()

# 7. Example Usage
if __name__ == '__main__':
    train_alpha_zero()
    print("Training complete!")
    
    # Example board setup (simplified)
    example_board = ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 
                     'wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr', 
                     ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 
                     'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 
                     'br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br']
    
    move, value = predict_move(example_board, ChessNN())
    print(f"Predicted move: {move}, Predicted value: {value}")
