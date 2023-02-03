def candidateEntity(candidate) -> dict:
    return {
        "id": str(candidate["_id"]),
        "first_name": candidate["first_name"],
        "last_name": candidate["last_name"],
        "email": candidate["email"],
        "UUID": candidate["UUID"],
        "career_level": candidate["career_level"],
        "job_major": candidate["job_major"],
        "years_of_experience": candidate["years_of_experience"],
        "degree_type": candidate["degree_type"],
        "skills": candidate["skills"],
        "nationality": candidate["nationality"],
        "city": candidate["city"],
        "salary": candidate["salary"],
        "gender": candidate["gender"],
        "created_at": candidate["created_at"],
        "updated_at": candidate["updated_at"]
    }


def candidateListEntity(candidates) -> list:
    return [candidateEntity(candidate) for candidate in candidates]

