import pytest

from water_utility_billing import calculate_water_bill, check_meter_tampering


def test_calculate_bill_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_water_bill({}, 10)
    with pytest.raises(ValueError):
        calculate_water_bill([], -1)


def test_calculate_bill_skips_inactive_accounts_and_prices_usage_tiers():
    accounts = [
        {"is_active": False, "usage_blocks": [1000]},
        {"is_active": True, "usage_blocks": [30, 60]},
        {"is_active": True, "is_commercial": True, "usage_blocks": [120]},
        {"is_active": True, "usage_blocks": [120, 10]},
    ]

    assert calculate_water_bill(accounts, 10) == {
        "total_billed": 1185.0,
        "status": "NORMAL",
    }


def test_calculate_bill_flags_invalid_usage_and_applies_large_leak_waiver():
    accounts = [
        {"is_active": True, "usage_blocks": [0, -1, 120], "has_leak_waiver": True},
        {"is_active": True, "usage_blocks": [0, -1, 0]},
    ]

    assert calculate_water_bill(accounts, 10) == {
        "total_billed": 510.0,
        "status": "EXCESSIVE_FLAGS",
    }


def test_calculate_bill_returns_no_activity_for_no_active_accounts():
    assert calculate_water_bill([], 0) == {
        "total_billed": 0.0,
        "status": "NO_ACTIVITY",
    }


def test_calculate_bill_marks_more_than_five_flags_as_excessive():
    account = {"is_active": True, "usage_blocks": [0, 0, 0, 0, 0, 0]}
    assert calculate_water_bill([account], 0)["status"] == "EXCESSIVE_FLAGS"


def test_check_meter_tampering_handles_empty_input_and_empty_meters():
    assert check_meter_tampering([]) == "NO_DATA"
    assert check_meter_tampering([[]]) == "CLEAR"


def test_check_meter_tampering_resets_count_and_detects_consecutive_reverse_flow():
    assert check_meter_tampering([[-1, 0, -1]]) == "CLEAR"
    assert check_meter_tampering([[1, -1, -2]]) == "TAMPER_SUSPECTED"

