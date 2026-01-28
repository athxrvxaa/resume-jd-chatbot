from typing import Dict

def final_match_score(
        rule_result: Dict[str,object],
        semantic_result: Dict[str,object],
        alpha: float = 0.6
) -> Dict[str,object]:
    
    rule_score = rule_result.get("match_score",0.0)
    semantic_score = semantic_result.get("semantic_score",0.0)

    beta = 1 - alpha

    final_score = round(
        (alpha * rule_score) + (beta * semantic_score) , 2
    )

    return{
        "final_score": final_score,
        "rule_score": rule_score,
        "semantic_score": semantic_score,
        "matched_skills": rule_result.get("matched_skills", []),
        "missing_skills": rule_result.get("missing_skills", []),
        "semantic_matches": semantic_result.get("matched_requirements", [])
    }