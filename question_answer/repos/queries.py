from typing import Iterable, Any


def select_query(
    table_name: str,
    table_fields: Iterable[str],
    specifiers: str | None = None,
    return_fields: str = "*",
) -> str:
    """
    Creates select SQL query of table 'table_name'

    Arguments:
        table_name: name of table
        table_fields: list of table's fields
        specifiers: string with specifiers separated with " ".
            If not provided, no data filtering would be performed
        return_fields: string with desired return fields separated with " ".
            "*" by default
    """
    if return_fields != "*":
        for return_field in return_fields.split():
            if return_field not in table_fields:
                raise ValueError(f"Return field {return_field} is not a field of '{table_name}' table")

    return_fields = ", ".join(return_fields.split())
    query = f"SELECT {return_fields} FROM {table_name}"
    if not specifiers:
        return query + ";"

    specifiers = specifiers.split()
    query += " WHERE"
    for i, specifier in enumerate(specifiers):
        if specifier not in table_fields:
            raise ValueError(f"Specifier '{specifier}' is not a field of '{table_name}' table")
        query += f" {specifier} = ?"
        if i != len(specifiers) - 1:
            query += " AND"

    return query + ";"


def insert_query(
    table_name: str,
    table_fields: Iterable[str],
) -> str:
    """
    Creates insert SQL query to table table_name

    Arguments:
        table_name: name of table
        table_fields: list of table fields to insert
    """
    joined_fields = ", ".join(table_fields)
    value_placeholders = ", ".join("?" for _ in range(len(table_fields)))
    query = f"INSERT INTO {table_name} ({joined_fields}) VALUES ({value_placeholders});"
    return query


def update_query(
    table_name: str,
    table_fields: Iterable[str],
    updating_data: dict[str, Any],
    specifiers: str | None = None,
) -> str:
    query = f"UPDATE {table_name} SET"

    for field, value in updating_data.items():
        if isinstance(value, str):
            query += f" {field} = '{value}'"
        else:
            query += f" {field} = {value}"
    if not specifiers:
        return query + ";"

    specifiers = specifiers.split()
    query += " WHERE"
    for i, specifier in enumerate(specifiers):
        if specifier not in table_fields:
            raise ValueError(f"Specifier '{specifier}' is not a field of '{table_name}' table")
        query += f" {specifier} = ?"
        if i != len(specifiers) - 1:
            query += " AND"

    return query
