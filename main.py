from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from test.test_database import *
import unittest, sqlite3

from app.resources import *
from app.resources import app as apis
from client.application import app as client

application = DispatcherMiddleware(apis, {
    '/shareit/client': client
})


if __name__ == "__main__":
    #app.run(debug=True, port=3000)
    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)