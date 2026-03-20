from typing import List, Dict


def detect_conflicts(new_meds: List[dict], old_meds: List[dict]) -> List[dict]:
    conflicts = []

    old_map = {}

    for med in old_meds:
        old_map[med["name"]] = med

    for med in new_meds:
        name = med["name"]

        if name in old_map:
            old = old_map[name]

        
            if med.get("dose") and old.get("dose"):
                if med["dose"] != old["dose"]:
                    conflicts.append({
                        "type": "dose_mismatch",
                        "medications": [name],
                    })

        
            if med["status"] != old["status"]:
                conflicts.append({
                    "type": "active_stopped",
                    "medications": [name],
                })

    return conflicts