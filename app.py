from flask import Flask, render_template, request
from find_route import find_route

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])

def index():
    if request.method == "POST":
        #get start station and end station from form
        origin = request.form["origin"]
        destination = request.form["destination"]
        #make sure start station and end station are not the same
        if origin != destination:
            directions, start_station, end_station = find_route(origin, destination)
            return render_template("results.html", directions = directions, start_station = start_station, end_station = end_station)
        else:
            return render_template("index.html", error = "Please choose a different start and end station.") 
    else:
        return render_template("index.html") 

if __name__ == '__main__':
    app.run()