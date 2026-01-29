from pydantic import BaseModel
from typing import List, Dict


class MatchResponse(BaseModel):
    final_score: float
    rule_score: float
    semantic_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    semantic_matches: List[Dict[str, object]]
