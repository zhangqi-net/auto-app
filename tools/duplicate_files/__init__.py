from flask import Blueprint

bp = Blueprint('duplicate_files', __name__, url_prefix='/tools/duplicate-files')

from . import routes 