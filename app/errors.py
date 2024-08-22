from flask import render_template, url_for
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template(
        'page_error.html',
        logo_img=url_for('static', filename='img/app_img/error_1.gif'),
        main_img=url_for('static', filename='img/app_img/404_1.gif'),
        type_error=404), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(
        'page_error.html',
        logo_img=url_for('static', filename='img/app_img/error_1.gif'),
        main_img=url_for('static', filename='img/app_img/error_2.gif'),
        type_error=500), 500
    