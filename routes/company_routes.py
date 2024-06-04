from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Company, db

company_bp = Blueprint('company_bp', __name__, url_prefix='/companies')

@company_bp.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        max_length = request.form['max_length']
        max_width = request.form['max_width']
        max_height = request.form['max_height']
        max_weight = request.form['max_weight']
        max_volumetric_weight = request.form['max_volumetric_weight']

        new_company = Company(
            name=name,
            category=category,
            max_length=max_length,
            max_width=max_width,
            max_height=max_height,
            max_weight=max_weight,
            max_volumetric_weight=max_volumetric_weight
        )

        db.session.add(new_company)
        db.session.commit()
        flash('Company added successfully!')
        return redirect(url_for('company_bp.manage_companies'))
    return render_template('add_company.html')

@company_bp.route('/companies', methods=['GET'])
def manage_companies():
    companies = Company.query.all()
    return render_template('manage_companies.html', companies=companies)

@company_bp.route('/edit_company/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == 'POST':
        company.name = request.form['name']
        company.category = request.form['category']
        company.max_length = request.form['max_length']
        company.max_width = request.form['max_width']
        company.max_height = request.form['max_height']
        company.max_weight = request.form['max_weight']

        db.session.commit()
        flash('Company updated successfully!')
        return redirect(url_for('company_bp.manage_companies'))
    return render_template('edit_company.html', company=company)

@company_bp.route('/delete_company/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('Company deleted successfully!')
    return redirect(url_for('company_bp.manage_companies'))
