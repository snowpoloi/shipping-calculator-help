from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.Enum('courier', 'transport'), nullable=False)
    max_length = db.Column(db.Float, nullable=True)
    max_width = db.Column(db.Float, nullable=True)
    max_height = db.Column(db.Float, nullable=True)
    max_weight = db.Column(db.Float, nullable=True)
    max_volumetric_weight = db.Column(db.Float, nullable=True)

    offers = db.relationship('Offer', back_populates='company', cascade="all, delete-orphan")
    postal_codes = db.relationship('CompanyPostalCode', back_populates='company', cascade="all, delete-orphan")

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    offer_type = db.Column(db.String(50), nullable=False)
    min_weight = db.Column(db.Float, nullable=True)
    max_weight = db.Column(db.Float, nullable=True)
    base_cost = db.Column(db.Float, nullable=False)
    extra_cost_per_kg = db.Column(db.Float, nullable=True)
    cubic_rate = db.Column(db.Float, nullable=True)
    min_charge = db.Column(db.Float, nullable=True)

    company = db.relationship('Company', back_populates='offers')
    postal_codes = db.relationship('OfferPostalCode', back_populates='offer', cascade="all, delete-orphan")

class PostalCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postal_code = db.Column(db.String(20), nullable=False, unique=True)
    area_name = db.Column(db.String(128), nullable=False)
    prefecture = db.Column(db.String(128), nullable=False)

    offer_postal_codes = db.relationship('OfferPostalCode', back_populates='postal_code', cascade="all, delete-orphan")
    company_postal_codes = db.relationship('CompanyPostalCode', back_populates='postal_code', cascade="all, delete-orphan")

class OfferPostalCode(db.Model):
    __tablename__ = 'offer_postal_code'
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), primary_key=True)
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.id'), primary_key=True)

    offer = db.relationship('Offer', back_populates='postal_codes')
    postal_code = db.relationship('PostalCode', back_populates='offer_postal_codes')

class CompanyPostalCode(db.Model):
    __tablename__ = 'company_postal_code'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.id'), nullable=False)
    status = db.Column(db.Enum('accessible', 'hard_to_reach', 'not_serviced'), nullable=False)

    company = db.relationship('Company', back_populates='postal_codes')
    postal_code = db.relationship('PostalCode', back_populates='company_postal_codes')