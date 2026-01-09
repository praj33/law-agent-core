def calculate_reward(vote: str, time_spent: int, follow_up: bool):
    reward = 0.0

    if vote == "up":
        reward += 1
    elif vote == "down":
        reward -= 1

    if time_spent > 60:
        reward += 0.5

    if follow_up:
        reward += 0.3

    return reward
