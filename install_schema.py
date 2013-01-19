#!/usr/bin/env python2.7
import os
import sqlite3
import config

db_filename = config.db_filename
schema_filename = config.db_filename

db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        print 'Creating schema'
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
    else:
        print 'Database exists, assume schema does, too.'
