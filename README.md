# SOMus: Sensibly Organized Music

Somus is a personal project of mine to establish a platform for music metadata tabulated and stored in a sensible way. Unlike Spotify and many other music services, composers, orchestras, arrangers, and soloists aren't all lumped under the single category of "artist", but rather their actual roles in a piece. This web application is written in Python with Django and is currently deployed on Heroku.

The deployed web application can be found at https://somus.herokuapp.com/.

## Setup
For production, the following environmental variables need to be set:
```
ALLOWED_HOSTS=.herokuapp.com
DATABASE_URL=<heroku already sets this up with a postgresql url>
SECRET_KEY=<your secret key>
SPOTIPY_CLIENT_ID=<your spotify client id>
SPOTIPY_CLIENT_SECRET=<your spotify client secret>
```
For local development, create a `.env` file with the following:
```
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=<whatever secret key you want>
DEBUG=on
```
