"""
Bradley-Terry Elo Rating Tournament Skill Client
Pure Python Standard Library implementation of Elo & Bradley-Terry Paired Comparison Models.
Maintains continuous skill ratings, matches candidates, and predicts pairwise head-to-head win probabilities.
"""

import math
from typing import List, Dict, Any, Tuple, Optional


class EloTournament:
    """
    Elo & Bradley-Terry tournament ranker for LLM agents / prompts / tool solutions.
    Expected score: E_A = 1 / (1 + 10^((R_B - R_A) / 400))
    Rating update: R_A' = R_A + K * (S_A - E_A)
    """

    def __init__(self, default_rating: float = 1500.0, k_factor: float = 32.0):
        self.default_rating = default_rating
        self.k_factor = k_factor
        self.ratings: Dict[str, float] = {}
        self.match_counts: Dict[str, int] = {}
        self.match_history: List[Dict[str, Any]] = []

    def get_rating(self, candidate: str) -> float:
        """Get current Elo rating of candidate."""
        return self.ratings.get(candidate, self.default_rating)

    def win_probability(self, candidate_a: str, candidate_b: str) -> float:
        """Compute expected probability of A beating B under Bradley-Terry / Elo."""
        r_a = self.get_rating(candidate_a)
        r_b = self.get_rating(candidate_b)
        return 1.0 / (1.0 + math.pow(10.0, (r_b - r_a) / 400.0))

    def record_match(self, candidate_a: str, candidate_b: str, score_a: float) -> Dict[str, Any]:
        """
        Record result of match between A and B.
        :param score_a: 1.0 if A wins, 0.5 for draw, 0.0 if B wins.
        """
        if not 0.0 <= score_a <= 1.0:
            raise ValueError("Score must be between 0.0 and 1.0")

        r_a = self.get_rating(candidate_a)
        r_b = self.get_rating(candidate_b)

        expected_a = self.win_probability(candidate_a, candidate_b)
        expected_b = 1.0 - expected_a
        score_b = 1.0 - score_a

        # Adaptive K-factor: higher for new candidates
        n_a = self.match_counts.get(candidate_a, 0)
        n_b = self.match_counts.get(candidate_b, 0)
        k_a = self.k_factor * 1.5 if n_a < 10 else self.k_factor
        k_b = self.k_factor * 1.5 if n_b < 10 else self.k_factor

        new_r_a = r_a + k_a * (score_a - expected_a)
        new_r_b = r_b + k_b * (score_b - expected_b)

        self.ratings[candidate_a] = new_r_a
        self.ratings[candidate_b] = new_r_b
        self.match_counts[candidate_a] = n_a + 1
        self.match_counts[candidate_b] = n_b + 1

        record = {
            "candidate_a": candidate_a,
            "candidate_b": candidate_b,
            "score_a": score_a,
            "old_rating_a": r_a,
            "old_rating_b": r_b,
            "new_rating_a": new_r_a,
            "new_rating_b": new_r_b,
            "delta_a": new_r_a - r_a,
            "delta_b": new_r_b - r_b
        }
        self.match_history.append(record)
        return record

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Return leaderboard sorted by rating descending."""
        candidates = sorted(self.ratings.keys(), key=lambda c: self.ratings[c], reverse=True)
        leaderboard = []
        for rank, c in enumerate(candidates, start=1):
            leaderboard.append({
                "rank": rank,
                "candidate": c,
                "rating": round(self.ratings[c], 1),
                "matches": self.match_counts.get(c, 0)
            })
        return leaderboard
