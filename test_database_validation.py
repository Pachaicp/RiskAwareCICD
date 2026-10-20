
from database_validator import validate_database


def test_safe_additive_migration_passes():
    result = validate_database(
        old_columns=["id", "name"],
        new_columns=["id", "name", "email"],
        sql_script="ALTER TABLE users ADD COLUMN email VARCHAR(255);",
    )

    assert result["status"] == "PASS"
    assert result["sql_analysis"]["is_destructive"] is False


def test_removed_column_is_blocked():
    result = validate_database(
        old_columns=["id", "name", "email"],
        new_columns=["id", "name"],
        sql_script="ALTER TABLE users DROP COLUMN email;",
    )

    assert result["status"] == "BLOCKED"
    assert result["schema_analysis"]["removed_columns"] == ["email"]


def test_drop_table_is_blocked():
    result = validate_database(
        old_columns=["id"],
        new_columns=["id"],
        sql_script="DROP TABLE users;",
    )

    assert result["status"] == "BLOCKED"
    assert result["sql_analysis"]["is_destructive"] is True
