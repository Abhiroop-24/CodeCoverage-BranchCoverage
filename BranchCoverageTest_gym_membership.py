import pytest
from gym_membership import membership_cost, can_enter, bmi_category

# ==============================================================================
# Comprehensive Branch Coverage Test Suite
# Every decision branch (True & False outcomes, compound conditions, edge cases)
# is systematically exercised to achieve 100% Branch Coverage.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Tests for membership_cost(plan, age, is_student, with_trainer)
# ------------------------------------------------------------------------------

def test_membership_cost_invalid_plan():
    """Branch: if plan not in PLAN_PRICE -> True"""
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 25, False, False)

def test_membership_cost_too_young():
    """Branch: if age < 14 -> True (Boundary: age 13)"""
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)

def test_membership_cost_boundary_youngest_allowed():
    """Branch: if age < 14 -> False (Boundary: age 14 exactly)"""
    assert membership_cost("monthly", 14, False, False) == 1500

def test_membership_cost_senior():
    """Branch: if age >= 60 -> True (senior gets 25% discount)"""
    # Boundary: age 60 exactly on quarterly plan (4000 - 1000 = 3000)
    assert membership_cost("quarterly", 60, False, False) == 3000

def test_membership_cost_student():
    """Branch: elif is_student -> True (student gets 10% discount when age < 60)"""
    assert membership_cost("monthly", 22, True, False) == 1350

def test_membership_cost_regular_adult():
    """Branch: neither senior nor student (no discount)"""
    assert membership_cost("monthly", 30, False, False) == 1500

def test_membership_cost_senior_and_student_precedence():
    """Branch check: senior discount takes precedence over student discount"""
    # 1500 - 375 = 1125
    assert membership_cost("monthly", 65, True, False) == 1125

def test_membership_cost_with_trainer_yearly():
    """
    Branches:
    - with_trainer == True
    - plan == 'yearly' (True: additional 500 discount on trainer)
    Base: 12000 + 2000 - 500 = 13500
    """
    assert membership_cost("yearly", 30, False, True) == 13500

def test_membership_cost_with_trainer_non_yearly():
    """
    Branches:
    - with_trainer == True
    - plan == 'yearly' (False: e.g. monthly plan, no trainer discount)
    Base: 1500 + 2000 = 3500
    """
    assert membership_cost("monthly", 30, False, True) == 3500

def test_membership_cost_without_trainer():
    """Branch: with_trainer == False"""
    assert membership_cost("yearly", 30, False, False) == 12000


# ------------------------------------------------------------------------------
# 2. Tests for can_enter(hour, plan_active, is_women_only_slot, gender)
# ------------------------------------------------------------------------------

def test_can_enter_inactive_plan():
    """Branch: if not plan_active -> True (returns False)"""
    assert can_enter(10, False, False, "M") is False

def test_can_enter_hour_below_opening():
    """Branch: if hour < 5 -> True (Boundary: 4, returns False)"""
    assert can_enter(4, True, False, "M") is False

def test_can_enter_hour_above_closing():
    """Branch: if hour > 22 -> True (Boundary: 23, returns False)"""
    assert can_enter(23, True, False, "M") is False

def test_can_enter_opening_boundary():
    """Branch: hour == 5 (opening boundary, passes time check)"""
    assert can_enter(5, True, False, "M") is True

def test_can_enter_closing_boundary():
    """Branch: hour == 22 (closing boundary, passes time check)"""
    assert can_enter(22, True, False, "M") is True

def test_can_enter_women_only_female():
    """Branch: is_women_only_slot == True, gender == 'F' (returns True)"""
    assert can_enter(14, True, True, "F") is True

def test_can_enter_women_only_male():
    """Branch: is_women_only_slot == True, gender != 'F' (returns False)"""
    assert can_enter(14, True, True, "M") is False

def test_can_enter_regular_slot():
    """Branch: is_women_only_slot == False (returns True for any gender)"""
    assert can_enter(14, True, False, "M") is True


# ------------------------------------------------------------------------------
# 3. Tests for bmi_category(weight_kg, height_m)
# ------------------------------------------------------------------------------

def test_bmi_category_invalid_height_zero():
    """Branch: if height_m <= 0 -> True (height = 0)"""
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(60, 0)

def test_bmi_category_invalid_height_negative():
    """Branch: if height_m <= 0 -> True (height < 0)"""
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(60, -1.75)

def test_bmi_category_underweight():
    """Branch: bmi < 18.5 -> True"""
    assert bmi_category(40, 1.7) == "underweight"

def test_bmi_category_normal():
    """Branch: 18.5 <= bmi < 25"""
    # 60 / (1.7 * 1.7) = 20.76
    assert bmi_category(60, 1.7) == "normal"

def test_bmi_category_overweight():
    """Branch: 25 <= bmi < 30"""
    # 75 / (1.7 * 1.7) = 25.95
    assert bmi_category(75, 1.7) == "overweight"

def test_bmi_category_obese():
    """Branch: bmi >= 30"""
    # 100 / (1.7 * 1.7) = 34.60
    assert bmi_category(100, 1.7) == "obese"
