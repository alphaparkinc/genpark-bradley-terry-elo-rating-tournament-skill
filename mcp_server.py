"""
MCP Server for Bradley-Terry Elo Rating Tournament Skill.
"""

import json
import sys
from client import EloTournament

TOURNAMENT = EloTournament()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "record_match",
                    "description": "Record a head-to-head match result between two agents/prompts",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "candidate_a": {"type": "string"},
                            "candidate_b": {"type": "string"},
                            "score_a": {"type": "number"}
                        },
                        "required": ["candidate_a", "candidate_b", "score_a"]
                    }
                },
                {
                    "name": "get_leaderboard",
                    "description": "Retrieve current Elo leaderboard",
                    "inputSchema": {
                        "type": "object"
                    }
                },
                {
                    "name": "win_probability",
                    "description": "Predict head-to-head win probability between two candidates",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "candidate_a": {"type": "string"},
                            "candidate_b": {"type": "string"}
                        },
                        "required": ["candidate_a", "candidate_b"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "record_match":
            res = TOURNAMENT.record_match(
                args["candidate_a"],
                args["candidate_b"],
                args["score_a"]
            )
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        elif tool_name == "get_leaderboard":
            res = TOURNAMENT.get_leaderboard()
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        elif tool_name == "win_probability":
            p = TOURNAMENT.win_probability(args["candidate_a"], args["candidate_b"])
            return {"content": [{"type": "text", "text": json.dumps({"win_probability": p})}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
