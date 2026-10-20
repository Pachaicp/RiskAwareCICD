
import re


def validate_schema(old_columns: list[str], new_columns: list[str]) -> dict:
    removed = sorted(set(old_columns) - set(new_columns))
    added = sorted(set(new_columns) - set(old_columns))

    if removed:
        return {
            "status": "BLOCKED",
            "schema_analysis": {
                "status": "REVIEW_REQUIRED",
                "removed_columns": removed,
                "added_columns": added,
                "message": (
                    "Existing columns were removed or renamed: "
                    + ", ".join(removed)
                ),
            },
        }

    return {
        "status": "PASS",
        "schema_analysis": {
            "status": "PASS",
            "removed_columns": [],
            "added_columns": added,
            "message": "No column removals detected.",
        },
    }


def analyze_sql(sql_script: str) -> dict:
    destructive_pattern = (
        r"\bDROP\s+(TABLE|COLUMN|DATABASE)\b"
        r"|\bTRUNCATE\s+TABLE\b"
    )

    matches = re.findall(
        destructive_pattern,
        sql_script,
        flags=re.IGNORECASE,
    )

    if matches:
        return {
            "status": "BLOCKED",
            "is_destructive": True,
            "warnings": [
                "Potentially destructive SQL operation detected."
            ],
            "recommendation": (
                "Review the migration and obtain database administrator "
                "approval before proceeding."
            ),
        }

    return {
        "status": "PASS",
        "is_destructive": False,
        "warnings": [],
        "recommendation": "No configured destructive SQL pattern detected.",
    }


def validate_database(
    old_columns: list[str],
    new_columns: list[str],
    sql_script: str,
) -> dict:
    schema = validate_schema(old_columns, new_columns)
    sql = analyze_sql(sql_script)

    blocked = (
        schema["status"] == "BLOCKED"
        or sql["status"] == "BLOCKED"
    )

    return {
        "status": "BLOCKED" if blocked else "PASS",
        "schema_analysis": schema["schema_analysis"],
        "sql_analysis": sql,
    }
