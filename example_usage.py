"""
Example usage of Bradley-Terry Elo Rating Tournament Skill.
"""

from client import EloTournament


def main():
    print("=== Bradley-Terry Elo Rating Tournament Demonstration ===")
    tournament = EloTournament(default_rating=1500.0, k_factor=32.0)

    # 4 Prompt Engineering Strategies competing head-to-head:
    # 1. Few-Shot CoT
    # 2. Zero-Shot
    # 3. ReAct Prompt
    # 4. Self-Refine
    matches = [
        ("Few-Shot CoT", "Zero-Shot", 1.0),
        ("ReAct Prompt", "Zero-Shot", 1.0),
        ("Self-Refine", "Few-Shot CoT", 1.0),
        ("Self-Refine", "ReAct Prompt", 0.5),  # Draw
        ("Few-Shot CoT", "Zero-Shot", 1.0),
        ("ReAct Prompt", "Few-Shot CoT", 1.0)
    ]

    print(f"Simulating {len(matches)} benchmark matches:\n")
    for a, b, s in matches:
        res = tournament.record_match(a, b, s)
        print(f"Match: {a:<14} vs {b:<14} | Score: {s} | {a} ({res['delta_a']:+.1f}) -> {res['new_rating_a']:.1f}")

    print("\n=== Current Leaderboard ===")
    leaderboard = tournament.get_leaderboard()
    for row in leaderboard:
        print(f"  #{row['rank']} {row['candidate']:<16} Elo: {row['rating']} ({row['matches']} matches)")

    # Predict future matchup
    p_win = tournament.win_probability("Self-Refine", "Zero-Shot")
    print(f"\nPredicted Win Probability 'Self-Refine' vs 'Zero-Shot': {p_win * 100:.1f}%")


if __name__ == "__main__":
    main()
