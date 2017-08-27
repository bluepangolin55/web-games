#!flask/bin/python
from main import app, socketio
# app.run(debug=True)

if __name__ == '__main__':
	print("App is starting..")
	socketio.run(app, port=80, debug=True)
