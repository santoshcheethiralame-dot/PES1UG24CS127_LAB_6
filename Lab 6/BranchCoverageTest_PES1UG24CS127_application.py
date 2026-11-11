from water_utility_billing import calculate_water_bill, check_meter_tampering


def test_account_and_base_fee_validation_branches():
    try:
        calculate_water_bill(None, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("non-list accounts should raise ValueError")

    try:
        calculate_water_bill([], -1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative base fee should raise ValueError")

    assert calculate_water_bill([], 0)["status"] == "NO_ACTIVITY"


def test_account_active_and_usage_range_branches():
    accounts = [
        {"is_active": False, "usage_blocks": [999]},
        {"is_active": True, "usage_blocks": [0, -2, 50, 51]},
        {"is_active": True, "is_commercial": True, "usage_blocks": [100, 101]},
        {"is_active": True, "is_commercial": False, "usage_blocks": [101, 1]},
    ]
    result = calculate_water_bill(accounts, 0)
    assert result == {"total_billed": 1260.5, "status": "NORMAL"}


def test_leak_waiver_and_bill_threshold_branches():
    accounts = [
        {"is_active": True, "usage_blocks": [50], "has_leak_waiver": True},
        {"is_active": True, "usage_blocks": [100], "has_leak_waiver": True},
        {"is_active": True, "usage_blocks": [120], "has_leak_waiver": True},
        {"is_active": True, "usage_blocks": [120], "has_leak_waiver": False},
    ]
    assert calculate_water_bill(accounts, 0) == {
        "total_billed": 1305.0,
        "status": "NORMAL",
    }


def test_flag_and_zero_total_status_branches():
    assert calculate_water_bill(
        [{"is_active": True, "usage_blocks": [0, 0, 0, 0, 0, 0]}], 0
    )["status"] == "EXCESSIVE_FLAGS"
    assert calculate_water_bill([{"is_active": False}], 0)["status"] == "NO_ACTIVITY"
    assert calculate_water_bill([{"is_active": True, "usage_blocks": [1]}], 0)["status"] == "NORMAL"


def test_meter_tampering_data_loop_and_reverse_flow_branches():
    assert check_meter_tampering([]) == "NO_DATA"
    assert check_meter_tampering([[]]) == "CLEAR"
    assert check_meter_tampering([[1, -1, 2, -1]]) == "CLEAR"
    assert check_meter_tampering([[-1, -2]]) == "TAMPER_SUSPECTED"


