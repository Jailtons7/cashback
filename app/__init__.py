from flask import Flask

from config.settings import Settings


app = Flask(__name__)
app.config.from_object(Settings)

