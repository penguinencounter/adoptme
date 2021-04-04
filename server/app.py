import os

import flask
from flask import Flask, request, Markup
import dbsearch

app = Flask(__name__, static_url_path='', static_folder='static')
log_path = os.path.abspath(os.path.expanduser("data/adoptme.log"))


def markup_log(line: str) -> str:
    """Add markup to log"""
    if '[' not in line:
        # Nothing to mark up.
        return line

    prefix, line = line.split('[', maxsplit=1)
    line, suffix = line.split(']', maxsplit=1)
    markup = []
    for t in line.split(','):
        t = t.strip()
        if t:
            markup.append(f'<a href="/record/{t}">{t}</a>')
    markup = ', '.join(markup)
    return f'{prefix}[{markup}]{suffix}'


def get_unique_records(records):
    """Find all the unique records. (by ID number)"""
    def records_similar(a, b):
        """Sort of like __eq__ but only looks at animal id numbers."""
        if a.animal_id == b.animal_id:
            return True
        return False
    processed = []
    individual_records = []
    for r in records:
        put_in = [True]
        for other in records:
            if r == other:
                continue
            if other in processed:
                continue
            if records_similar(r, other):
                put_in[0] = False
        put_in = put_in[0]
        if put_in:
            individual_records.append(r)
        processed.append(r)

    return individual_records


def fetch_logs(path: str = "/home/pi/data/adoptme.log"):
    file = []
    with open(path, 'r') as f:
        for line in f:
            file.append(Markup(markup_log(line)))
    return file[-51:]


@app.route('/')
def index():
    logs = fetch_logs(log_path)
    print(f"\nflask/index: {logs}")
    return flask.render_template("temp.html",
                                 logs=logs,
                                 logpath='/adoptme.log/')


@app.route('/adoptme.log/')
def log():
    file = [""]
    with open(log_path) as f:
        file[0] = f.read()
    return file[0]


@app.route("/popup/<animal_id>/")
def popup(animal_id):
    database = dbsearch.DBSearch("data/pets.pkl")
    results = database.search(0, animal_id)
    return flask.render_template("popup_record.html", records=[r for r in results])


@app.route('/grid/')
def checkerboard():
    records = dbsearch.DBSearch("data/pets.pkl").everything()
    records.reverse()
    records = get_unique_records(records)
    imaged_records = []
    for r in records:
        if os.path.exists(f"server/static/images/{r.animal_id}.jpg"):
            imaged_records.append(r)
    return flask.render_template("grid.html", records=imaged_records)


@app.route('/search/', methods=('GET', 'POST'))
def search():
    if request.method == 'GET':
        database = dbsearch.DBSearch("data/pets.pkl")
        return flask.render_template("search.html",
                                     possible_breeds=database.possible_breeds,
                                     possible_age_groups=database.possible_age_groups,
                                     possible_genders=database.possible_genders,
                                     possible_locations=database.possible_locations,
                                     possible_sources=database.possible_sources)
    elif request.method == 'POST':
        search_mode = request.form["search_mode"]
        search_term = request.form["search_term"]
        print(search_mode, search_term.lower())
        if search_term.lower() == "none":
            print("Turned the search term into a NoneType...")
            search_term = None
        database = dbsearch.DBSearch("data/pets.pkl")
        results = database.search(dbsearch.DBSearch.keyword_basic[search_mode], search_term)
        return flask.render_template("searchresults.html", records=[r for r in results])


@app.route("/record/<animal_id>/")
def record_show(animal_id):
    database = dbsearch.DBSearch("data/pets.pkl")
    results = database.search(0, animal_id)
    return flask.render_template("record_on_file.html", records=[r for r in results])


@app.route("/adv/")
def advanced_search():
    return flask.render_template("adv_search.html")


app.run("0.0.0.0", 8000, debug=True)
