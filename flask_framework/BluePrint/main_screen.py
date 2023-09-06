from flask import Blueprint
bp = Blueprint("main",__name__,url_prefix='/')


@bp.route('/games')
def Games():
    pass


@bp.route('/rank')
def Rank():
    pass


@bp.route('/library')
def Library():
    pass