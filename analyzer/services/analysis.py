def analyze_resume(resume_text, job_text):

    resume_tokens = set(resume_text.split())
    job_tokens = set(job_text.split())
    matched_keywords = []

    score = 0
    for token in resume_tokens:
        if token in job_tokens:
            score += 1
            matched_keywords.append(token)

    return score, matched_keywords