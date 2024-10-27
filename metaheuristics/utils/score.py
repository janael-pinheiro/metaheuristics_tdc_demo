from Levenshtein import distance


def compute_score(target_solution: str, neighbor: str) -> int:
    return distance(target_solution.lower(), neighbor.lower())