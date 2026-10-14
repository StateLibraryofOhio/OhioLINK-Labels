import json
import argparse
import sys
from collections import defaultdict

# id is optional: sort_libraries.py assigns one to entries that omit it.
REQUIRED_FIELDS = (
    "libid", "name", "address", "address2",
    "city", "state", "zip", "hub", "route",
)

# Fields that must carry a non-empty value (address2 is legitimately blank for most entries).
NON_EMPTY_FIELDS = ("libid", "name", "address", "city", "state", "hub")


def validate_libraries(input_path):
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON — {e}", file=sys.stderr)
        return False

    if not isinstance(data, list):
        print("Error: Expected a JSON array at the root level.", file=sys.stderr)
        return False

    errors = []
    ids = defaultdict(list)
    libids = defaultdict(list)

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"entry #{index} is {type(item).__name__}, not an object")
            continue

        label = item.get("name") or f"entry #{index}"

        missing = [field for field in REQUIRED_FIELDS if field not in item]
        if missing:
            errors.append(f"{label} is missing field(s): {', '.join(missing)}")

        for field in NON_EMPTY_FIELDS:
            if field in item and not str(item[field] or "").strip():
                errors.append(f"{label} has an empty {field}")

        for field in ("id", "zip", "route"):
            if field in item and not isinstance(item[field], int):
                errors.append(f"{label} has a non-integer {field}: {item[field]!r}")

        if isinstance(item.get("id"), int):
            if item["id"] < 0:
                errors.append(f"{label} has a negative id: {item['id']}")
            ids[item["id"]].append(label)

        if "libid" in item:
            libids[str(item["libid"]).strip()].append(label)

    for id_value, labels in ids.items():
        if len(labels) > 1:
            errors.append(f"id {id_value} is used by {len(labels)} entries ({', '.join(labels)})")

    for libid, labels in libids.items():
        if len(labels) > 1:
            errors.append(f"libid {libid!r} is used by {len(labels)} entries ({', '.join(labels)})")

    if errors:
        print("Error: output.json validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return False

    print(f"✓ Validated {len(data)} entries — required fields present, ids and libids unique.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate that a library JSON array is well-formed with unique ids and libids. Entries may omit id; the sort workflow assigns one."
    )
    parser.add_argument("input", help="Path to the source JSON file.")

    args = parser.parse_args()
    sys.exit(0 if validate_libraries(args.input) else 1)
