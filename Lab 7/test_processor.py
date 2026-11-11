from hypothesis import given, strategies as st

from processor import (
    format_billing_summary,
    parse_consumption_readings,
    sanitize_meter_id,
)


@given(st.one_of(st.text(), st.none()))
def test_sanitize_meter_id_no_crash(value):
    try:
        result = sanitize_meter_id(value)
    except ValueError:
        return

    assert isinstance(value, str)
    assert isinstance(result, str)
    expected = value.strip()
    for character in "!@#$%":
        expected = expected.replace(character, "")
    assert result == expected.upper()


@given(st.one_of(st.text(), st.none()))
def test_parse_consumption_readings_safe(value):
    try:
        result = parse_consumption_readings(value)
    except ValueError:
        return

    assert isinstance(value, str)
    assert isinstance(result, list)
    assert result == [int(part.strip()) for part in value.split(",")]


@given(st.one_of(st.text(), st.none()))
def test_format_billing_summary_safe(value):
    try:
        result = format_billing_summary(value)
    except ValueError:
        return

    assert isinstance(value, str)
    parts = value.split(":")
    assert len(parts) == 3
    customer_name, units, zone = parts
    assert customer_name.strip()
    assert zone.strip()
    assert result == (
        f"Customer {customer_name.strip()} billed "
        f"{int(units) * 2} USD in {zone.strip()}"
    )
