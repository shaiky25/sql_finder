import io
import os

directory = os.path.dirname(__file__)
filename = os.path.join(directory, 'test.sql')

def sql_finder():
    with io.open(filename, mode='r', encoding='utf-8') as f:
        sql = f.read()
        sql = sql.replace('\n', ' ')
        sql = sql.replace('\r', ' ')
        sql = sql.replace('\t', ' ')

        return sql

def sql_finder2():
    processed_lines = []
    sqls = []
    with io.open(filename, mode='r', encoding='utf-8') as f:
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


if __name__ == '__main__':
    list_sqls = sql_finder2()
    for sql_query in list_sqls:
        print(sql_query)
        if sql_query.strip().startswith('UPDATE'):
            check_for_where(sql_query, 'UPDATE')
        elif sql_query.strip().startswith('DELETE'):
            check_for_where(sql_query, 'DELETE')