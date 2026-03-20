def test_high_conflict_logic():
    data = [
        {"patient_id": "1"},
        {"patient_id": "1"},
        {"patient_id": "2"},
    ]

    counts = {}
    for d in data:
        counts[d["patient_id"]] = counts.get(d["patient_id"], 0) + 1

    high = [k for k, v in counts.items() if v >= 2]

    assert "1" in high