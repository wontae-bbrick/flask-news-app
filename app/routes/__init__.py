from flask import Blueprint
bp = Blueprint('routes', __name__)
# from .ai import *
# from .sto import *
from .keyword import *
from .news import *