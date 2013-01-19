-- Schema for game
CREATE TABLE game ( 
  name TEXT primary key,
  starttime INTEGER,
  completed INTEGER
);

CREATE TABLE player (
  phonenumber TEXT,
  name TEXT,
  description TEXT,
  valid INTEGER
);

CREATE TABLE game_player (
  name TEXT not null references game(name),
  phonenumber TEXT not null references player(phonenumber),
  status INTEGER not null default 1, -- alive, 0 = dead
  next TEXT not null references game(name)
);
