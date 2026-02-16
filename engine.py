import random
from typing import Tuple, List, Callable


Move = str  # "C" or "D"
History = List[Move]


class IteratedPrisonersDilemma:
    def __init__(
        self,
        payoff_matrix: dict = None,
        rounds: int = 200,
        noise: float = 0.0,
        seed: int = None,
    ):
        """
        payoff_matrix: dict with keys (move1, move2) -> (score1, score2)
        rounds: number of rounds per match
        noise: probability that a move flips (0.0 to 1.0)
        seed: random seed for reproducibility
        """
        if payoff_matrix is None:
            # Default standard PD payoffs
            payoff_matrix = {
                ("C", "C"): (3, 3),
                ("C", "D"): (0, 5),
                ("D", "C"): (5, 0),
                ("D", "D"): (1, 1),
            }

        self.payoff_matrix = payoff_matrix
        self.rounds = rounds
        self.noise = noise

        if seed is not None:
            random.seed(seed)

    def _apply_noise(self, move: Move) -> Move:
        """Flip move with probability equal to self.noise."""
        if random.random() < self.noise:
            return "D" if move == "C" else "C"
        return move

    def play_match(
        self,
        strategy1: Callable,
        strategy2: Callable,
    ) -> Tuple[int, int, History, History]:
        """
        Plays a full match between two strategies.

        Returns:
            total_score1, total_score2, history1, history2
        """
        history1: History = []
        history2: History = []

        total_score1 = 0
        total_score2 = 0

        for _ in range(self.rounds):
            move1 = strategy1(history1, history2)
            move2 = strategy2(history2, history1)

            # Apply noise
            move1 = self._apply_noise(move1)
            move2 = self._apply_noise(move2)

            history1.append(move1)
            history2.append(move2)

            score1, score2 = self.payoff_matrix[(move1, move2)]
            total_score1 += score1
            total_score2 += score2

        return total_score1, total_score2, history1, history2
