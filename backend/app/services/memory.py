from typing import List, Dict


class ChatMemory:
    def __init__(self, max_turns: int = 3):
        self.history: List[Dict[str, str]] = []
        self.max_turns = max_turns

    def add_turn(self, user: str, assistant: str):
        self.history.append({
            "user": user,
            "assistant": assistant
        })

        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def format_history(self) -> str:
        if not self.history:
            return "No prior conversation."

        lines = []
        for turn in self.history:
            lines.append(f"User: {turn['user']}")
            lines.append(f"Assistant: {turn['assistant']}")

        return "\n".join(lines)
