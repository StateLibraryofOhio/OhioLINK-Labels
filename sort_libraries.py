import json
import argparse
import sys


def sort_libraries(input_path, output_path=None):
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON — {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("Error: Expected a JSON array at the root level.", file=sys.stderr)
        sys.exit(1)

    # Sort alphabetically by name (case-insensitive)
    sorted_data = sorted(data, key=lambda x: (x.get("name") or "").casefold())

    # Collect all existing valid ids
    existing_ids = {
        item["id"] for item in sorted_data
        if isinstance(item.get("id"), int) and item["id"] > 0
    }

    # Assign ids only to entries missing a valid one, starting from max + 1
    next_id = max(existing_ids, default=0) + 1
    assigned = 0
    for item in sorted_data:
        if not isinstance(item.get("id"), int) or item["id"] < 0:
            item["id"] = next_id
            next_id += 1
            assigned += 1

    destination = output_path or input_path
    with open(destination, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✓ Sorted {len(sorted_data)} entries and wrote to '{destination}'.")
    if assigned:
        print(f"  {assigned} new id(s) assigned.")
    else:
        print(f"  All entries already had an id — none assigned.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sort a library JSON array alphabetically by name and assign missing ids."
    )
    parser.add_argument("input", help="Path to the source JSON file.")
    parser.add_argument(
        "--output", "-o",
        help="Path for the sorted output file. Defaults to overwriting the input file.",
        default=None
    )

    args = parser.parse_args()
    sort_libraries(args.input, args.output)
