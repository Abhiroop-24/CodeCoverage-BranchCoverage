import pytest
from gym_membership import membership_cost, can_enter, bmi_category

# --- Starter Tests ---
def test_monthly_plan():
    assert membership_cost("monthly", 30, False, False) == 1500

def test_can_enter():
    assert can_enter(10, True, False, "M") is True

# --- Targeted Line Coverage Tests (executes remaining unvisited lines) ---

def test_unknown_plan():
    # executes line 6: raise ValueError("unknown plan")
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("invalid_plan", 25, False, False)

def test_too_young():
    # executes line 8: raise ValueError("too young")
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 10, False, False)

def test_senior_discount():
    # executes line 11: cost -= cost // 4
    assert membership_cost("monthly", 65, False, False) == 1125

def test_student_discount():
    # executes line 13: cost -= cost // 10
    assert membership_cost("monthly", 20, True, False) == 1350

def test_trainer_yearly_addon():
    # executes line 15-17: cost += 2000, if plan == "yearly": cost -= 500
    assert membership_cost("yearly", 30, False, True) == 13500

def test_entry_inactive():
    # executes line 23: return False
    assert can_enter(10, False, False, "M") is False

def test_entry_outside_hours():
    # executes line 25: return False (hour < 5)
    assert can_enter(4, True, False, "M") is False

def test_entry_women_only_slot():
    # executes line 27: return gender == "F"
    assert can_enter(10, True, True, "F") is True

def test_bmi_invalid_height():
    # executes line 33: raise ValueError("invalid height")
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(60, 0)

def test_bmi_categories_all_lines():
    # executes lines 36, 38, 40, 41
    assert bmi_category(40, 1.7) == "underweight"   # < 18.5
    assert bmi_category(60, 1.7) == "normal"        # < 25
    assert bmi_category(75, 1.7) == "overweight"    # < 30
    assert bmi_category(95, 1.7) == "obese"         # >= 30
