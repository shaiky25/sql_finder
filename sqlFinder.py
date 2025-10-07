import io
import os
from pathlib import Path

directory = Path("sqls")


def sql_finder(file_name):
    with io.open(file_name, mode='r', encoding='utf-8') as f:
        sql = f.read()
        sql = sql.replace('\n', ' ')
        sql = sql.replace('\r', ' ')
        sql = sql.replace('\t', ' ')

        return sql

def sql_finder2(file_name):
    processed_lines = []
    sqls = []
    with io.open(file_name, mode='r', encoding='utf-8') as f:
        for line in f:
            # Remove leading/trailing whitespace, including the newline character
            query_string = line.strip()
            comment = (query_string.startswith('-') or query_string.startswith('#') or query_string.startswith(
                '/') or query_string.startswith('*'))
            # Check if the stripped line starts with the specified prefix
            if not comment:
                processed_lines.append(query_string)
    sql = ''
    for word in processed_lines:
        if not word.endswith(';'):
            sql = sql + word.strip() + ' '
        else:
            sql = sql + word.strip()
            sqls.append(sql)
            sql = ''
    return sqls



def split_query(query_string, delimiter):
    list_queries = query_string.split(delimiter)
    filtered_queries = []
    for query_string in list_queries:
        if query_string.strip() != '':
            filtered_queries.append(query_string)
    return filtered_queries


def check_for_where(sql_string, keyword):
    try:
        sql_string = sql_string.strip()
        sql_string[len(keyword):].index('WHERE')
    except:
        raise ValueError(f"WHERE CLAUSE MISSING IN {keyword} query: '{sql_string}'")


def run_validation_rules():
    for filename in os.listdir(directory):
        if filename.endswith('.sql'):
            filename = os.path.join(directory, filename)
            list_sqls = sql_finder2(filename)
            for sql_query in list_sqls:
                # print(sql_query)
                try:
                    if sql_query.strip().startswith('UPDATE'):
                        check_for_where(sql_query, 'UPDATE')
                    elif sql_query.strip().startswith('DELETE'):
                        check_for_where(sql_query, 'DELETE')
                    valid_sql = True
                except Exception as e:
                    valid_sql = False
                    print(f'In FILE {filename} "{e} "')
    return valid_sql

if __name__ == '__main__':
    run_validation_rules()
