#!/usr/bin/env python2.7
from flask import Flask, request, redirect
import twilio.twiml
import config
import sqlite3
import os

app = Flask(__name__)

conn = sqlite3.connect(config.db_filename)
cursor = conn.cursor()

players = {}
games = {}

@app.route("/", methods=['GET', 'POST'])
def register():
  resp_str = ""
  number = request.values.get('From', None)
  # Remove '+' from start
  number = number[1:]
  body = request.values.get('Body', None)
  resp_str = parse_msg(number, body)
  if resp_str == "":
    print "Not sure how to parse " + body
  else:
    print resp_str
  resp = twilio.twiml.Response()
  resp.sms(resp_str)
  return str(resp)

def parse_msg(number, msg):
  # check for join
  if len(msg) > 5 and msg[0:5].lower() == "join ":
    game = msg[5:].strip()
    if join_game(number, game):
      return "Successfully joined " + game
    else:
      return "Did not join " + game
  return ""

def join_game(number, game_name):
  # check to make sure number isnt in game
  return True

if __name__ == "__main__":
  conn = sqlite3.connect(config.db_filename)
  cursor = conn.cursor()
  app.debug = True
  app.run(host='0.0.0.0')
