from app.services.conflict_detection import detect_conflicts


def test_dose_mismatch():
    old = [{"name": "druga", "dose": "10mg", "status": "active"}]
    new = [{"name": "druga", "dose": "20mg", "status": "active"}]

    conflicts = detect_conflicts(new, old)

    assert len(conflicts) == 1
    assert conflicts[0]["type"] == "dose_mismatch"