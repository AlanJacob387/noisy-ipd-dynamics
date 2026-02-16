import random

# Utility

def cooperate():
    return "C"
def defect():
    return "D"

# Unconditional Strategies

def clara(history_self, history_opponent):
    """
    Always cooperates.
    """
    return cooperate()

def victor(history_self, history_opponent):
    """
    Always defects.
    """
    return defect()

# Reciprocal Strategies

def miles(history_self, history_opponent):
    """
    Tit-for-Tat.
    Cooperates initially.
    """
    if not history_opponent:
        return cooperate()
    return history_opponent[-1]

def elena(history_self, history_opponent):
    """
    Tit-for-Tat.
    Defects initially.
    """
    if not history_opponent:
        return defect()
    return history_opponent[-1]

def isabella(history_self, history_opponent, forgiveness_index=0.1):
    """
    Tit-for-Tat.
    Cooperates initially.
    If opponent defected last round, forgives with probability forgiveness_index (default values = 0.1).
    """
    if not history_opponent:
        return cooperate()
    if history_opponent[-1] == "D":
        if random.random() < forgiveness_index:
            return cooperate()
        return defect()
    return cooperate()

def nathan(history_self, history_opponent):
    """
    Two-Tits-for-Tat.
    Cooperates initially.
    Defects only if opponent defected in the last two consecutive rounds.
    """
    if len(history_opponent) < 2:
        return cooperate()
    if history_opponent[-1] == "D" and history_opponent[-2] == "D":
        return defect()
    return cooperate()

# Punitive Strategies

def gabriel(history_self, history_opponent):
    """
    Cooperates until opponent defects once.
    Then defects forever.
    """
    if "D" in history_opponent:
        return defect()
    return cooperate()

# Stochastic Strategies

def iris(history_self, history_opponent, cooperation_index=0.5):
    """
    Random strategy.
    Cooperates with probability cooperation_index (default value = 0.5).
    """
    return cooperate() if random.random() < cooperation_index else defect()

# Adaptive Strategies

def lucas(history_self, history_opponent):
    """
    Pavlov (Win-Stay, Lose-Shift).
    Repeats previous move if payoff was good, switch otherwise.
    Cooperates initially.
    """
    if not history_self:
        return cooperate()
    last_self = history_self[-1]
    last_opponent = history_opponent[-1]
    if (last_self == cooperate() and last_opponent == cooperate()) or (last_self == defect() and last_opponent == cooperate()):
        return last_self
    else:
        return defect() if last_self == cooperate() else cooperate()


def samuel(history_self, history_opponent):
    """
    Majority strategy.
    Cooperates initially.
    Cooperates if opponent has cooperated more times than defected.
    Otherwise defects.
    """
    if not history_opponent:
        return cooperate()

    cooperations = history_opponent.count("C")
    defections = history_opponent.count("D")

    if cooperations >= defections:
        return cooperate()
    return defect()

# Novel Strategies

def emily(history_self, history_opponent, W=50):
    """
    Adapts to random noise.
    Punishes sustained defection.
    Forgives isolated defection (likely noise).
    Escapes nutual defection traps.
    """
    t = len(history_self)
    if t==0:
        return cooperate()
    # Rolling window
    w = min(W,t)
    self_w = history_self[-w:]
    opponent_w = history_opponent[-w:]
    d_rate =opponent_w.count(defect())/w if w else 0
    # Opponent's current defection streak
    streak = 0
    for i in reversed(history_opponent):
        if i==defect():
            streak += 1
        else:
            break
    # Noise proxy: isolated C-D-C
    isolated = 0
    for i in range(1, w - 1):
        if opponent_w[i] == defect() and opponent_w[i - 1] == cooperate() and opponent_w[i + 1] == cooperate():
            isolated += 1
    isolated_ratio = (isolated / opponent_w.count(defect())) if opponent_w.count(defect()) > 0 else 0.0
    isolated_ratio = max(0.0, min(1.0, isolated_ratio))
    payoff = {
        (cooperate(), cooperate()): 3,
        (cooperate(), defect()): 0,
        (defect(), cooperate()): 5,
        (defect(), defect()): 1,
    }
    # Emperical profitability
    c_payoffs = []
    d_payoffs = []
    for m,o in zip(self_w, opponent_w):
        p = payoff[(m,o)]
        if m==cooperate():
            c_payoffs.append(p)
        else:
            d_payoffs.append(p)
    avgC = sum(c_payoffs) / len(c_payoffs) if c_payoffs else 0.0
    avgD = sum(d_payoffs) / len(d_payoffs) if d_payoffs else 0.0
    # If cooperation is being exploited, switch
    if len(c_payoffs) >= max(5, w // 3) and avgC < 2.0 and d_rate > 0.25:
        return defect()
        # Heavy defection opponent
    if d_rate > 0.60:
        return defect()
    # Escape mutual defection
    if history_opponent[-1] == defect() and history_self[-1] == defect():
        repair_p = 0.05 + 0.30 * isolated_ratio
        return cooperate() if random.random() < repair_p else defect()
    # Handle opponent defection
    if history_opponent[-1] == defect():
        if streak >= 5:
            return defect()
        forgive_p = 0.15 + 0.50 * isolated_ratio
        forgive_p *= max(0.0, 1.0 - d_rate)
        return cooperate() if random.random() < forgive_p else defect()
    return cooperate()
