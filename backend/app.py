from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  
from os import environ

app = Flask(__name__)
CORS(app)  
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Song(db.Model):
  __tablename__ = 'songs'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=False, nullable=False)
  artist = db.Column(db.String(120), unique=False, nullable=False)
  genre = db.Column(db.String(120), unique=False, nullable=True)

  def json(self):
    return {'id': self.id,'name': self.name, 'artist': self.artist, 'genre': self.genre}

db.create_all()

# test
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

@app.route('/api/flask/songs', methods=['POST'])
def create_song():
  try:
    data = request.get_json()
    new_song = Song(name=data['name'], artist=data['artist'], genre=data.get('genre'))
    db.session.add(new_song)
    db.session.commit()

    return jsonify({
        'id': new_song.id,
        'name': new_song.name,
        'artist': new_song.artist,
        'genre': new_song.genre
    }), 201
  except Exception as e:
      return make_response(jsonify({'message': 'error creating song', 'error': str(e)}), 500)

@app.route('/api/flask/songs', methods=['GET'])
def get_songs():
  try:
    songs = Song.query.all()
    songs_data = [{'id': song.id, 'name': song.name, 'artist': song.email, 'genre': song.genre} for song in songs]
    return jsonify(songs_data), 200
  except Exception as e:
    return make_response(jsonify({'message': 'error getting songs', 'error': str(e)}), 500)

@app.route('/api/flask/songs/<int:id>', methods=['DELETE'])
def delete_song(id):
  try:
    song = Song.query.filter_by(id=id).first()
    if song:
      db.session.delete(song)
      db.session.commit()
      return make_response(jsonify({'message': 'song deleted'}), 200)
    return make_response(jsonify({'message': 'song not found'}), 404)
  except Exception as e:
    return make_response(jsonify({'message': 'error deleting song', 'error': str(e)}), 500)