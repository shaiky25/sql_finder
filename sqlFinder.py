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


def check_for_create(list_of_queries, keyword,index):
    query = list_of_queries[index]
    table_name = query[len(keyword):].strip()
    if '/' in table_name:
        table_name = table_name.replace('/', '')
    # print("table_name: ", table_name)
    string_to_check = 'CREATE TABLE '+ table_name
    for query_string in list_of_queries[index:]:
        if string_to_check in query_string.strip() :
            valid_query = True
            break
        else:
            valid_query = False
    if not valid_query:
        raise ValueError(f"CREATE TABLE {table_name} not found after {keyword} in the file.")




def check_for_grant(sql_query, param):
    pass


def run_validation_rules():
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
                            check_for_create(list_sqls,'DROP TABLE IF EXISTS',index)
                        else:
                            index = list_sqls.index(sql_query)
                            check_for_create(list_sqls,'DROP TABLE',index)
                    elif sql_query.startswith('GRANT'):
                        check_for_grant(sql_query, 'GRANT')
                        
                    valid_sql = True
                except Exception as e:
                    valid_sql = False
                    print(f'In FILE {filename} "{e} "')
    return valid_sql

if __name__ == '__main__':
    run_validation_rules()
