from typing import List


def generate_improvements(missing_skills: List[str]) -> List[str]:
    suggestions = []

    for skill in missing_skills:
        if skill.lower() == "docker":
            suggestions.append(
                "Add Docker by containerizing one of your ML projects or mentioning model deployment using Docker."
            )
        elif skill.lower() == "pytorch":
            suggestions.append(
                "PyTorch is important for ML roles. Consider adding a small PyTorch-based project or rewriting an existing one using PyTorch."
            )
        elif skill.lower() == "sql":
            suggestions.append(
                "Explicitly mention SQL usage such as joins, aggregations, or real datasets queried."
            )
        else:
            suggestions.append(
                f"Highlight or add experience with {skill} if you have used it in any academic or personal project."
            )

    return suggestions
