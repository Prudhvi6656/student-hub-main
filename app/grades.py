"""Grade maths on a 10-point scale (CGPA), kept free of Flask for easy testing."""


def percentage_to_points(pct):
    if pct is None:
        return None
    for floor, points in ((90, 10), (80, 9), (70, 8), (60, 7), (50, 6), (40, 5)):
        if pct >= floor:
            return points
    return 0


def course_percentage(assessments):
    """Weighted percentage over graded assessments only (None if nothing graded)."""
    graded = [a for a in assessments if a.score is not None and a.max_score > 0]
    total_weight = sum(a.weight for a in graded)
    if not total_weight:
        return None
    return sum(a.score / a.max_score * a.weight for a in graded) / total_weight * 100


def cgpa(courses):
    """Credit-weighted average of grade points across courses that have grades."""
    total_credits = points_sum = 0
    for c in courses:
        points = percentage_to_points(course_percentage(c.assessments))
        if points is not None:
            total_credits += c.credits
            points_sum += points * c.credits
    return round(points_sum / total_credits, 2) if total_credits else None


def needed_score(assessments, target_pct):
    """Average % needed on ungraded assessments to finish at target_pct (None if none pending)."""
    pending_w = sum(a.weight for a in assessments if a.score is None)
    if not pending_w:
        return None
    done = [a for a in assessments if a.score is not None and a.max_score > 0]
    total_w = pending_w + sum(a.weight for a in done)
    earned = sum(a.score / a.max_score * a.weight for a in done)
    return (target_pct / 100 * total_w - earned) / pending_w * 100
