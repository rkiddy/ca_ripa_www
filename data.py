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
    context = dict()

    sql = "select * from ripa_counties;"
    counties = db_exec(conn, sql)

    rows = list()

    for county in counties:

        sql = f"select count(0) as count from ripa_summaries_{county['code']};"
        count = db_exec(conn, sql)[0]['count']

        row = dict(county)
        row['count'] = count

        sql = f"select distinct(YEAR_OF_STOP) as year from ripa_summaries_{county['code']};"
        years = [str(r['year']) for r in db_exec(conn, sql)]

        row['years'] = ', '.join(years)

        rows.append(row)

    context['counties'] = rows

    return context


def ripa_data():
    results = {}
    return results
