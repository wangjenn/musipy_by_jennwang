from flask import render_template
from .initialize import app, estimator, song_names, song_cosines
from .views import main as main_blueprint

# Register the blueprint
app.register_blueprint(main_blueprint)

# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404
