import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout

#Example test cases:
def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600

def test_no_bonus():
    assert no_claim_bonus(0) == 0

#Write the rest of the test cases so that the code is 90- 100% covered.
# annual_premium: line coverage 
def test_unknown_car_type():
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)

def test_driver_too_young():
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)

def test_young_driver_surcharge():
    
    assert annual_premium("hatchback", 20, 1, False) == 12000

def test_senior_driver_surcharge():
   
    assert annual_premium("sedan", 65, 1, False) == 14000

def test_no_claims_discount():
    
    assert annual_premium("suv", 30, 0, False) == 12000

def test_many_claims_doubles():
    
    assert annual_premium("sedan", 30, 3, False) == 24000

def test_anti_theft_discount():
    
    assert annual_premium("sedan", 30, 1, True) == 11500

# no_claim_bonus: line coverage 
def test_bonus_negative_years():
    with pytest.raises(ValueError):
        no_claim_bonus(-1)

def test_bonus_tiers():
    assert no_claim_bonus(6) == 50
    assert no_claim_bonus(4) == 35
    assert no_claim_bonus(2) == 20
    assert no_claim_bonus(0) == 0

#  claim_payout: line coverage 
def test_payout_negative_amount():
    with pytest.raises(ValueError):
        claim_payout(-100, 100000, 1000, False)

def test_payout_total_loss():
    assert claim_payout(5000, 100000, 1000, True) == 100000

def test_payout_below_deductible():
    assert claim_payout(500, 100000, 1000, False) == 0

def test_payout_normal():
    assert claim_payout(5000, 100000, 1000, False) == 4000

def test_payout_capped_at_insured_value():
    assert claim_payout(150000, 100000, 1000, False) == 100000

#annual_premium: branch coverage 
def test_age_18_boundary_valid():
    
    assert annual_premium("hatchback", 18, 0, False) == 9600

def test_age_24_still_young():
    assert annual_premium("hatchback", 24, 1, False) == 12000

def test_age_25_no_surcharge():
    
    assert annual_premium("hatchback", 25, 1, False) == 8000

def test_age_59_no_surcharge():
    assert annual_premium("sedan", 59, 1, False) == 12000

def test_age_60_boundary_surcharge():
    assert annual_premium("sedan", 60, 1, False) == 14000

def test_two_claims_no_change():
   
    assert annual_premium("suv", 30, 2, False) == 15000

def test_three_claims_boundary():
    assert annual_premium("suv", 30, 3, False) == 30000

def test_all_adjustments_combined():
    
    assert annual_premium("hatchback", 20, 0, True) == 9100

def test_senior_no_claims_discount():
    
    assert annual_premium("sedan", 60, 0, False) == 11200

def test_young_many_claims():
    
    assert annual_premium("hatchback", 24, 3, False) == 24000

# no_claim_bonus: branch boundaries 
@pytest.mark.parametrize("years, expected", [
    (0, 0), (1, 20), (2, 20), (3, 35), (4, 35), (5, 50), (10, 50),
])
def test_bonus_boundaries(years, expected):
    assert no_claim_bonus(years) == expected

# claim_payout: branch coverage 
def test_payout_negative_deductible():
    # second half of the `or` condition
    with pytest.raises(ValueError):
        claim_payout(5000, 100000, -1, False)

def test_payout_damage_equals_deductible():
    assert claim_payout(1000, 100000, 1000, False) == 0

def test_payout_just_above_deductible():
    assert claim_payout(1001, 100000, 1000, False) == 1

def test_payout_equals_insured_value():
    
    assert claim_payout(101000, 100000, 1000, False) == 100000

def test_payout_zero_damage_zero_deductible():
    assert claim_payout(0, 100000, 0, False) == 0
