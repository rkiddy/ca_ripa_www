
import sys

from dotenv import dotenv_values
from flask import Flask, jsonify
from jinja2 import Environment, PackageLoader

cfg = dotenv_values(".env")

sys.path.append(f"{cfg['APP_HOME']}")
import data

ripa = Flask(__name__)
application = ripa
env = Environment(loader=PackageLoader('ripa'))


@ripa.route(f"/{cfg['WWW']}/")
def ripa_main():
    main = env.get_template('ripa_list.html')
    context = data.ripa_data_main()
    return main.render(**context)


@ripa.route(f"/{cfg['WWW']}/rest/")
def ripa_rest():
    rest_data = data.ripa_data()
    return jsonify(rest_data)


@ripa.route(f"/{cfg['WWW']}/county/<num>")
def ripa_county(num):
    main = env.get_template('ripa_list.html')
    context = data.ripa_agencies(num)
    return main.render(**context)


@ripa.route(f"/{cfg['WWW']}/agencies/")
def ripa_agencies():
    main = env.get_template('ripa_list.html')
    context = data.ripa_agencies()
    return main.render(**context)


if __name__ == '__main__':
    ripa.run(port=8080)
