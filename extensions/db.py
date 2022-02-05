from flask_mongoengine import MongoEngine


def init_db():
    db = MongoEngine()
    return db
