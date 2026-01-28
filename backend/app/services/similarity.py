from typing import Set,Dict

def skill_gap_analysis(
        resume_skills: Set[str],
        jd_skills: Set[str]
) -> Dict[str , object]:
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    if not jd_skills:
        score = 0.0
    else:
        score = round(len(matched) / len(jd_skills) , 2)

    return {
        "match_score":score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing)
    }