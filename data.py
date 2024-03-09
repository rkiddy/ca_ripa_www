from dotenv import dotenv_values
from flask import request
from sqlalchemy import create_engine, inspect

cfg = dotenv_values(".env")

con_engine = create_engine(f"mysql+pymysql://{cfg['USR']}:{cfg['PWD']}@{cfg['HOST']}/{cfg['DB']}")
conn = con_engine.connect()


def db_exec(engine, sql):
    # print(f"sql: {sql}")
    if sql.strip().startswith('select'):
        return [dict(r) for r in engine.execute(sql).fetchall()]
    else:
        return engine.execute(sql)


def ripa_data_main():
    results = dict()

    results['title'] = 'All Counties'

    sql = """
         select substr(AGENCY_ORI,3,3) as code_num,
                (select name from ripa_counties where code = code_num) as name,
                count(0) as count,
                min(DATE_OF_STOP) as min_date,
                max(DATE_OF_STOP) as max_date
                from ripa_summaries group by code_num order by code_num
         """
    results['entities'] = db_exec(conn, sql)

    for result in results['entities']:
        result['code_href'] = f"county/{result['code_num']}"

    return results


def ripa_data():
    results = dict()
    return results


def ripa_agencies(num = None):
    results = dict()

    if num is None:
        results['title'] = 'All Law Enforcement Agencies'

        sql = """
            select AGENCY_ORI as code_num,
                   (select name from ripa_counties where code = code_num) as name,
                   count(0) as count,
                   min(DATE_OF_STOP) as min_date,
                   max(DATE_OF_STOP) as max_date
                   from ripa_summaries group by code_num order by code_num
            """
    else:
        results['title'] = f"Law Enforcement Agencies - County: XXX"

        sql = f"""
            select AGENCY_ORI as code_num,
                   (select name from ripa_counties where code = code_num) as name,
                   count(0) as count,
                   min(DATE_OF_STOP) as min_date,
                   max(DATE_OF_STOP) as max_date
                   from ripa_summaries
                   where AGENCY_ORI like 'CA{num}%%'
                   group by code_num order by code_num
            """
    agencies = db_exec(conn, sql)

    if results['title'].endswith('XXX'):
        sql = f"select name from ripa_counties where code = '{num}'"
        name = db_exec(conn, sql)[0]['name']
        results['title'] = results['title'].replace('XXX', name)

    sql = """
          select distinct(concat(AGENCY_ORI, '|', AGENCY_NAME)) as code_and_name
          from ripa_summaries
          """
    for row in db_exec(conn, sql):
        parts = row['code_and_name'].split('|')
        for agency in agencies:
            if agency['code_num'] == parts[0]:
                agency['name'] = parts[1]

    results['entities'] = agencies

    return results
