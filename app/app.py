from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import time

app = Flask(__name__)


def filler(input):
    test={'test':f'this job ({input}) has been processed'}
    return test


# @app.route("/", methods=["GET", "POST"])
# def index():
#     """Return the homepage."""
    
#     if request.method == "POST":
        
#         jobSearch = request.form["jobInput"]
#         print(jobSearch)
#         result=filler(jobSearch)

#         # string=request

#         # return jsonify(result)
#         return render_template('index.html', result=result)
#     return render_template("index.html")


@app.route('/')
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route('/results', methods=["GET", "POST"])
def send():
    if request.method == "POST":
        jobSearch = request.form["jobInput"]
        result=filler(jobSearch)
        return render_template('results.html', result=result)
    # return redirect('results.html')

# @app.route('/results', methods=['GET', 'POST'])
# def results():
#     return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)