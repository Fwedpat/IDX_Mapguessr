from app import app
from flask import render_template, redirect, session, url_for
import os
import random
from flask import jsonify, request

app.secret_key = 'AmongUS!!!!!'

@app.route('/')
def hello_world():
    return render_template('homepage.html')

@app.route('/game')
def game():
    return redirect(url_for('play_game'))  # Redirect to the 'play_game' route

@app.route('/play_game')
def play_game():
    return render_template('game.html')  # Render the game.html template

@app.route('/levelDetails')
def levelDetails():
    levels_folder = 'C:/Users/fredd/OneDrive/Documents/Mapguessr/FlaskApp/app/static/levels'
    level_folders = os.listdir(levels_folder)
    random_level_folder = random.choice(level_folders)
    level_details_file = os.path.join(levels_folder, random_level_folder, 'levelDetails.txt')

    with open(level_details_file, 'r') as file:
        level_details = file.read()
    year = level_details.split('\n')[0].split(',')[0]
    long = level_details.split('\n')[0].split(',')[1]
    lat = level_details.split('\n')[0].split(',')[2]
    description = level_details.split('\n')[1]
    
    level_coords_file = os.path.join(levels_folder, random_level_folder, 'imageCoords.txt')

    with open(level_coords_file, 'r') as file:
        coords = file.read()
    min_coords = coords.split('\n')[0]
    max_coords = coords.split('\n')[1]
    min_lat = min_coords.split(',')[0]
    min_long = min_coords.split(',')[1]
    max_lat = max_coords.split(',')[0]
    max_long = max_coords.split(',')[1]

    return jsonify(year, long, lat, description, min_lat, min_long, max_lat, max_long)


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    data = request.get_json()
    session['year'] = data['year']
    session['long'] = data['long']
    session['lat'] = data['lat']
    session['description'] = data['description']
    session['min_lat'] = data['min_lat']
    session['min_long'] = data['min_long']
    session['max_lat'] = data['max_lat']
    session['max_long'] = data['max_long']
    session['distance'] = data['distance']
    return redirect(url_for('results_page'))  # Redirect to the 'guess_page' route with additional variables


@app.route('/getRoundDetails', methods=['GET'])
def another_route():
    

    
    year = session.get('year')
    long = session.get('long')
    lat = session.get('lat')
    print(str(long) + ' ' + str(lat))
    description = session.get('description')
    min_lat = session.get('min_lat')
    min_long = session.get('min_long')
    max_lat = session.get('max_lat')
    max_long = session.get('max_long')
    distance = session.get('distance')



    return jsonify(year=year, long=long, lat=lat, description=description, min_lat=min_lat, min_long=min_long, max_lat=max_lat, max_long=max_long, distance=distance)   


@app.route('/results_page')
def results_page():
    return render_template('roundResults.html')  # Render the game.html template