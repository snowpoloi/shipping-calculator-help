from .main_routes import main_bp
from .company_routes import company_bp
from .offer_routes import offer_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(company_bp, url_prefix='/companies')
    app.register_blueprint(offer_bp, url_prefix='/offers')
