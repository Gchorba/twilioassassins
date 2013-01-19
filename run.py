from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

players = {}
games = {}

@app.route("/", methods=['GET', 'POST'])
def register():
  number = request.values.get('From', None)
  name = request.values.get('Body', None)
  players[number] = name;
  resp = twilio.twiml.Response()
  resp.sms("Hello, " + name)
  return str(resp)

if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0')
