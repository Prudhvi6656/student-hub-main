from types import SimpleNamespace as NS

from app.grades import cgpa, course_percentage, needed_score, percentage_to_points


def test_points_scale():
    assert percentage_to_points(95) == 10
    assert percentage_to_points(80) == 9
    assert percentage_to_points(41) == 5
    assert percentage_to_points(10) == 0
    assert percentage_to_points(None) is None


def test_course_percentage_ignores_ungraded():
    items = [NS(score=40, max_score=50, weight=20),
             NS(score=80, max_score=100, weight=30),
             NS(score=None, max_score=100, weight=50)]
    assert round(course_percentage(items), 2) == 80.0
    assert course_percentage([NS(score=None, max_score=100, weight=10)]) is None


def test_cgpa_is_credit_weighted():
    a = NS(credits=4, assessments=[NS(score=90, max_score=100, weight=100)])  # 10
    b = NS(credits=2, assessments=[NS(score=60, max_score=100, weight=100)])  # 7
    c = NS(credits=3, assessments=[])                                         # ignored
    assert cgpa([a, b, c]) == 9.0
    assert cgpa([c]) is None


def test_needed_score_for_target():
    done = NS(score=40, max_score=50, weight=40)   # 80% of 40 weight = 32 earned
    pending = NS(score=None, max_score=100, weight=60)
    assert round(needed_score([done, pending], 90), 1) == 96.7
    assert needed_score([done], 90) is None
    assert needed_score([done, pending], 50) < 50
