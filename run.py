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
  try:
    # See if we already have player in the database
    cursor.execute("SELECT name FROM player WHERE phonenumber =:num", {"num" : number})
    playername = cursor.fetchone()

    # See if game exists in database
    cursor.execute("SELECT name FROM game WHERE name =:name", {"name" : game_name})
    game = cursor.fetchone()
    if (game == None):
      raise FailJoin("Game does not exist")

    # Add player to player table if not already exists
    if (playername == None):
      cursor.execute("INSERT INTO player VALUES (?,'', '', 0)", number)
      conn.commit()

    # Check if the player is already in the game
    cursor.execute("SELECT name FROM game_player WHERE name = ? AND phonenumber = ?", playername, game_name)
    already_in_game = cursor.fetchone()
    if not already_in_game == None:
      raise FailJoin("Player already registered in game")

    # Add player to the game
    cursor.execute("INSERT INTO game_player VALUES (?, ?, 1, '')", game_name, number)
    conn.commit()
  except sqlite3.OperationalError, msg:
    print msg
    raise FailJoin("Database error")
  return playername

# Exceptions
class FailJoin(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

if __name__ == "__main__":
  conn = sqlite3.connect(config.db_filename)
  cursor = conn.cursor()
  app.debug = True
  app.run(host='0.0.0.0')
