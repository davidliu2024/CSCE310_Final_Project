from flask import Flask
from flask_cors import CORS

def create_app() -> Flask:
    """
    Creates an application instance (for use by mod_wsgi)
    """
    app = Flask(__name__)
    CORS(app)

    from . import auth, db, users, programs, events, applications, classes, certifications, intern_apps, internships
    app.register_blueprint(auth.bp)
    app.register_blueprint(db.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(programs.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(applications.bp)
    app.register_blueprint(classes.bp)
    app.register_blueprint(certifications.bp)
    app.register_blueprint(internships.bp)
    app.register_blueprint(intern_apps.bp)


    return app