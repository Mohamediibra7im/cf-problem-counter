from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional
from api import MIN_RATING, MAX_RATING, RATING_STEP


def process_submissions(
    submissions: List[Dict],
    min_rating: int = MIN_RATING,
    max_rating: int = MAX_RATING,
    rating_step: int = RATING_STEP,
    min_year: int = 2000,
    max_year: int = 2025,
) -> Dict[int, Dict[int, int]]:

    year_rating_counts = defaultdict(lambda: defaultdict(int))
    solved_problems = set()

    if not submissions:
        return year_rating_counts

    for submission in submissions:
        if submission["verdict"] == "OK":
            problem = submission["problem"]
            if "rating" in problem and min_rating <= problem["rating"] <= max_rating:
                problem_id = f"{problem['contestId']}{problem['index']}"
                if problem_id not in solved_problems:
                    solved_problems.add(problem_id)
                    submission_time = datetime.fromtimestamp(
                        submission["creationTimeSeconds"]
                    )
                    year = submission_time.year
                    if min_year <= year <= max_year:
                        year_rating_counts[year][problem["rating"]] += 1

    return year_rating_counts
