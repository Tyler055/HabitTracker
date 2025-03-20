from routes.auth import auth as auth_blueprint
from routes.chat import chat as chat_blueprint
from routes.files import files as files_blueprint
from routes.habits import habits as habits_blueprint
from routes.dashboard import dashboard as dashboard_blueprint

def register_blueprints(app):
    """Register all blueprints with the app."""
    blueprints = [
        (auth_blueprint, "/auth"),
        (chat_blueprint, "/chat"),
        (files_blueprint, "/files"),
        (habits_blueprint, "/habits"),
        (dashboard_blueprint, "/dashboard"),
    ]

    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

    return app
