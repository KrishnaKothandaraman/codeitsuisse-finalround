from flask import Flask
app = Flask(__name__)

import codeitsuisse.routes.parasite
import codeitsuisse.routes.tictactoe
import codeitsuisse.routes.asteroids
import codeitsuisse.routes.square
import codeitsuisse.routes.fixedrace
import codeitsuisse.routes.gridmap
import codeitsuisse.routes.decoder

