#!/usr/bin/env python2.7
from flask import Flask, request, redirect
import twilio.twiml
import config

app = Flask(__name__)

conn = sqlite3.connect(config.db_filename)
cursor = conn.cursor()

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
