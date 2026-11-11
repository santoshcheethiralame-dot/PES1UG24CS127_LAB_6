def sanitize_meter_id(meter_id):
    if not isinstance(meter_id, str):
        raise ValueError("Meter ID must be text")

    meter_id = meter_id.strip()
    for character in "!@#$%":
        meter_id = meter_id.replace(character, "")
    meter_id = meter_id.upper()
    if not meter_id:
        raise ValueError("Meter ID cannot be empty")
    return meter_id


def parse_consumption_readings(readings_csv):
    if not isinstance(readings_csv, str) or not readings_csv.strip():
        raise ValueError("Readings must be a non-empty comma-separated string")

    readings = []
    for reading in readings_csv.split(","):
        reading = reading.strip()
        if not reading:
            raise ValueError("Readings cannot contain empty values")
        try:
            readings.append(int(reading))
        except ValueError as error:
            raise ValueError("Each reading must be an integer") from error
    return readings


def format_billing_summary(account_record):
    if not isinstance(account_record, str):
        raise ValueError("Account record must be text")

    parts = account_record.split(":")
    if len(parts) != 3:
        raise ValueError("Account record must use Name:Usage:Zone format")

    customer_name, units_text, zone = (part.strip() for part in parts)
    if not customer_name or not zone:
        raise ValueError("Customer name and zone cannot be empty")
    try:
        units = int(units_text)
    except ValueError as error:
        raise ValueError("Usage must be an integer") from error
    if units < 0:
        raise ValueError("Usage cannot be negative")

    return f"Customer {customer_name} billed {units * 2} USD in {zone}"


def main():
    print("==== Running sanitize_meter_id ====")
    raw_id = input("Enter a meter ID with prefixes (!,@,#,$,%): ")
    try:
        clean_id = sanitize_meter_id(raw_id)
        print("Sanitized Meter ID:", clean_id)
    except ValueError as error:
        print("Invalid meter ID:", error)

    print("\n==== Running parse_consumption_readings ====")
    csv_input = input("Enter consumption readings (e.g. 10,25,30): ")
    try:
        readings_list = parse_consumption_readings(csv_input)
        print("Parsed Readings:", readings_list)
    except ValueError as error:
        print("Invalid consumption readings:", error)

    print("\n==== Running format_billing_summary ====")
    summary_input = input("Enter account record (Name:Usage:Zone): ")
    try:
        summary = format_billing_summary(summary_input)
        print("Billing Summary:", summary)
    except ValueError as error:
        print("Invalid account record:", error)


if __name__ == "__main__":
    main()
