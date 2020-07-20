from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    make_response)
import time

from run import run_all

app = Flask(__name__)


@app.route('/')
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route('/results', methods=["GET", "POST"])
def send():
    if request.method == "POST":
        jobSearch = request.form["jobInput"]

        ####scrape
        result, position, count_of_jobs = run_all(jobSearch)
        #result = make_response(jsonify(result), 200)



        return render_template('results.html', result=result, position=position, count_of_jobs=count_of_jobs)


if __name__ == '__main__':
    app.run(debug=True)
