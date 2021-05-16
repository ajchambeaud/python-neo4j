from neo4j import GraphDatabase
import os
import atexit

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class NeoDB(Singleton):
    driver=None

    def getDriver(self):
        if (self.driver != None):
            return self.driver

        USER = os.getenv('DATABASE_USERNAME')
        PASSWORD = os.getenv('DATABASE_PASSWORD')
        DB_URL = os.getenv('DATABASE_URL')
        
        self.driver = GraphDatabase.driver(DB_URL, auth=(USER, PASSWORD))

        return self.driver

    def getSession(self):
        return self.getDriver().session()

    def close(self):
        if (self.driver != None):
            self.driver.close()

def exit_handler():
    NeoDB().close()

atexit.register(exit_handler)
