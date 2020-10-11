from flask import Blueprint, render_template, request
import os
from .tasks import make_file,scrape
bp = Blueprint("all", __name__)

@bp.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@bp.route("/<string:fname>/<string:content>")
def makefile(fname, content):
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    make_file.delay(fpath, content)
    return f"Find your file @ <code>{fpath}</code>"

@bp.route('/test', methods=['POST'])
def rev():
    if request.method == 'POST':
        keyword = request.form['keyword']
        asin = request.form['asin']
        result = scrape.delay(keyword, asin)
        return result.get()

        # return

