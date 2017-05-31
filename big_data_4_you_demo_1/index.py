from flask import Flask, render_template, request, jsonify, json
from RSprova import Recommendation
app = Flask(__name__)

global r


def index_to_title(obj_ref, indexes):
    return [{j: (obj_ref.movies_df.loc[j][1] + " || " + obj_ref.movies_df.loc[j][2])} for j in indexes]


@app.after_request
def add_header(req):
    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers["Cache-Control"] = 'public, max-age=0'
    return req


@app.route('/')
def hello():
    k = Recommendation('00000', [1, 2, 3, 4, 5])
    preset_movie = [43, 5, 45, 34, 23, 65, 76, 87, 123, 456, 234, 55]
    # return render_template('index.html', pre_select=index_to_title(k, preset_movie),
    #                        movie_list = '-'.join([str(l) for l in preset_movie]))
    # return json.dumps(index_to_title(k,preset_movie))
    return render_template('new_index.html')


@app.route('/init/')
def init():
    k = Recommendation('00000', [1, 2, 3, 4, 5])
    preset_movie = [43, 5, 45, 34, 23, 65, 76, 87, 123, 456, 234, 55]
    return json.dumps(index_to_title(k, preset_movie))


@app.route('/initialize/<flags>/<indexes>')
def next_movie(flags, indexes):
    global r

    if len(flags) > 1:
        r = Recommendation(flags, [int(j) for j in indexes.split('-')])
        # return str(r.next_movie(-1,1))
        return json.dumps(r.next_movie(-1, 1))

    if flags == '-':
        # return str(r.next_movie(int(indexes), 0))
        return json.dumps(r.next_movie(int(indexes), 0))

    # return str(r.next_movie(int(indexes), 1))
    return json.dumps(r.next_movie(int(indexes), 1))
    

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
