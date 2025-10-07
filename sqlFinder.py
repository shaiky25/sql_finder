import io
import os
from pathlib import Path

directory = Path("sqls")


def sql_finder(file_name):
    """
    Read a SQL file and return its content as a single string with whitespace normalized.

    This function reads a SQL file, removes newlines, carriage returns, and tabs,
    and replaces them with spaces to create a single-line SQL string.

    Args:
        file_name (str): Path to the SQL file to read

    Returns:
        str: The SQL content as a single string with normalized whitespace

    Raises:
        IOError: If the file cannot be opened or read
    """
    with io.open(file_name, mode='r', encoding='utf-8') as f:
        sql = f.read()
        sql = sql.replace('\n', ' ')
        sql = sql.replace('\r', ' ')
        sql = sql.replace('\t', ' ')

        return sql


def sql_finder2(file_name):
    """
    Parse a SQL file and extract individual SQL queries.

    This function reads a SQL file line by line, filters out comments (lines starting
    with -, #, /*, or */), and groups lines into complete SQL queries. Queries are
    terminated by semicolons (;) or forward slashes (/).

    Args:
        file_name (str): Path to the SQL file to parse

    Returns:
        list[str]: List of complete SQL queries found in the file

    Raises:
        IOError: If the file cannot be opened or read
    """
    processed_lines = []
    sqls = []
    with io.open(file_name, mode='r', encoding='utf-8') as f:
        for line in f:

            # Remove leading/trailing whitespace, including the newline character
            query_string = line.strip()
            comment = (query_string.startswith('-') or query_string.startswith('#') or query_string.startswith(
                '/*') or query_string.startswith('*/'))
            # Check if the stripped line starts with the specified prefix
            if not comment:
                processed_lines.append(query_string)
    sql = ''
    for word in processed_lines:

        if not (word.endswith(';') or word == "/"):

            sql = sql + word.strip() + ' '
        else:
            sql = sql + word.strip()
            sql = sql.strip()
            sqls.append(sql)
            sql = ''
    # print(sqls)
    return sqls


def split_query(query_string, delimiter):
    """
    Split a query string by delimiter and filter out empty queries.

    This function splits a query string using the specified delimiter and returns
    a list of non-empty queries after stripping whitespace.

    Args:
        query_string (str): The query string to split
        delimiter (str): The delimiter to use for splitting

    Returns:
        list[str]: List of non-empty queries after splitting and filtering
    """
    list_queries = query_string.split(delimiter)
    filtered_queries = []
    for query_string in list_queries:
        if query_string.strip() != '':
            filtered_queries.append(query_string)
    return filtered_queries


def check_for_where(sql_string, keyword):
    """
    Validate that a SQL query contains a WHERE clause.

    This function checks if a SQL query (UPDATE or DELETE) contains a WHERE clause
    after the specified keyword. Raises a ValueError if WHERE clause is missing.

    Args:
        sql_string (str): The SQL query string to validate
        keyword (str): The SQL keyword (e.g., 'UPDATE', 'DELETE') to check after

    Raises:
        ValueError: If WHERE clause is missing in the query
    """
    try:
        sql_string = sql_string.strip()
        sql_string[len(keyword):].index('WHERE')
    except:
        raise ValueError(f"WHERE CLAUSE MISSING IN {keyword} query: '{sql_string}'")


def check_for_create(list_of_queries, keyword, index):
    """
    Validate that a DROP TABLE query has a corresponding CREATE TABLE query.

    This function checks if a DROP TABLE query has a corresponding CREATE TABLE
    statement later in the list of queries. It extracts the table name from the
    DROP statement and searches for a matching CREATE TABLE statement.

    Args:
        list_of_queries (list[str]): List of SQL queries to search through
        keyword (str): The DROP keyword ('DROP TABLE' or 'DROP TABLE IF EXISTS')
        index (int): Index of the DROP query in the list

    Raises:
        ValueError: If corresponding CREATE TABLE statement is not found
    """
    query = list_of_queries[index]
    table_name = query[len(keyword):].strip()
    if '/' in table_name:
        table_name = table_name.replace('/', '')
    # print("table_name: ", table_name)
    string_to_check = 'CREATE TABLE ' + table_name
    for query_string in list_of_queries[index:]:
        if string_to_check in query_string.strip():
            valid_query = True
            break
        else:
            valid_query = False
    if not valid_query:
        raise ValueError(f"CREATE TABLE {table_name} not found after {keyword} in the file.")


def check_for_grant(sql_query, param):
    """
    Validate GRANT SQL queries.

    This function is a placeholder for validating GRANT statements.
    Currently not implemented.

    Args:
        sql_query (str): The GRANT SQL query to validate
        param (str): Additional parameter for validation (currently unused)

    Todo:
        Implement validation logic for GRANT statements
    """
    pass


def run_validation_rules():
    """
    Run validation rules on all SQL files in the configured directory.

    This function processes all .sql files in the 'sqls' directory and validates
    them according to specific rules:
    - UPDATE queries must have WHERE clauses
    - DELETE queries must have WHERE clauses
    - DROP TABLE queries must have corresponding CREATE TABLE statements
    - GRANT queries are validated (placeholder implementation)

    Returns:
        bool: True if all validation rules pass, False if any fail

    Note:
        Errors are printed to stdout but do not stop execution
    """
    for filename in os.listdir(directory):
        if filename.endswith('.sql'):
            # print(filename)
            filename = os.path.join(directory, filename)
            list_sqls = sql_finder2(filename)
            # print(list_sqls)
            for sql_query in list_sqls:
                sql_query = sql_query.strip()
                # print(sql_query)
                try:
                    valid_sql = False
                    if sql_query.startswith('UPDATE'):
                        check_for_where(sql_query, 'UPDATE')
                    elif sql_query.startswith('DELETE'):
                        check_for_where(sql_query, 'DELETE')
                    elif sql_query.startswith('DROP TABLE'):

                        if sql_query.startswith('DROP TABLE IF EXISTS'):
                            index = list_sqls.index(sql_query)
                            check_for_create(list_sqls, 'DROP TABLE IF EXISTS', index)
                        else:
                            index = list_sqls.index(sql_query)
                            check_for_create(list_sqls, 'DROP TABLE', index)
                    elif sql_query.startswith('GRANT'):
                        check_for_grant(sql_query, 'GRANT')

                    valid_sql = True
                except Exception as e:
                    valid_sql = False
                    print(f'In FILE {filename} "{e} "')
    return valid_sql


if __name__ == '__main__':
    run_validation_rules()
