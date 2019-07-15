#!/usr/bin/env python3
import sqlite3


class Database:
    def __init__(self, hlr_loc):
        self.db = sqlite3.connect(hlr_loc)
        self.db_cursor = self.db.cursor()

        #self.subscribers = []
        self.IMSIs = []


    def get_new_users(self):
        for user in self.db_cursor.execute("SELECT * FROM Subscriber"):
            if user[3] not in self.IMSIs and user[3] != None and user[3] != 999999999999999:
                self.IMSIs.append(user[3])
                #self.subscribers.append(user)
                yield user


    def get_subscribers(self):
        subscribers = []

        for user in self.db_cursor.execute("SELECT * FROM Subscriber"):
            if user[3] != None and user[3] != 999999999999999:
                subscribers.append(user)

        return subscribers
