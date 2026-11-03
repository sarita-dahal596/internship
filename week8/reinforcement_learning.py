
import random

# Five positions: 0, 1, 2, 3, 4
states = 5

# Actions: 0 = left, 1 = right
actions = 2

# Q-table stores learned action values
q_table = [
    [0.0, 0.0] for _ in range(states)
]

learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.2

# Train for 1000 episodes
for episode in range(1000):
    position = 0

    while position != 4:

        # Explore or choose the best known action
        if random.random() < epsilon:
            action = random.randint(0, 1)
        else:
            action = q_table[position].index(
                max(q_table[position])
            )

        # Perform the selected action
        if action == 1:
            next_position = min(position + 1, 4)
        else:
            next_position = max(position - 1, 0)

        # Reward reaching the goal
        reward = 10 if next_position == 4 else -1

        # Goal is a terminal state
        future_reward = (
            0 if next_position == 4
            else max(q_table[next_position])
        )

        # Q-learning update
        old_value = q_table[position][action]

        q_table[position][action] = old_value + learning_rate * (
            reward + discount_factor * future_reward - old_value
        )

        position = next_position

print("Learned Q-table:")
for state, values in enumerate(q_table):
    print(f"State {state}: {values}")

# Test learned behavior without exploration
position = 0
path = [position]

while position != 4:
    action = q_table[position].index(max(q_table[position]))

    if action == 1:
        position = min(position + 1, 4)
    else:
        position = max(position - 1, 0)

    path.append(position)

print("Learned path:", path)
