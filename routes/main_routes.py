from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Offer, Company, PostalCode
import os
import csv
from werkzeug.utils import secure_filename

main_bp = Blueprint('main_bp', __name__)

UPLOAD_FOLDER = '/var/www/shipping_calculator/uploads'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    companies = Company.query.all()
    return render_template('index.html', companies=companies)

@main_bp.route('/calculate', methods=['POST'])
def calculate():
    total_weight = request.form.get('weight')
    if total_weight:
        total_weight = float(total_weight)
    else:
        flash('Total weight is required')
        return redirect(url_for('main_bp.index'))

    total_volume = request.form.get('volume')
    if total_volume:
        total_volume = float(total_volume)
    else:
        total_volume = None

    num_packages = int(request.form['num_packages'])
    include_cubic_rate = 'include_cubic_rate' in request.form

    packages = []
    for i in range(num_packages):
        input_type = request.form.get(f'input_type_{i}')
        length = request.form.get(f'length_{i}')
        width = request.form.get(f'width_{i}')
        height = request.form.get(f'height_{i}')
        weight = request.form.get(f'weight_{i}')
        volume = request.form.get(f'volume_{i}')

        if length:
            length = float(length)
        if width:
            width = float(width)
        if height:
            height = float(height)
        if weight:
            weight = float(weight)
        if volume:
            volume = float(volume)
        packages.append({
            'input_type': input_type,
            'length': length,
            'width': width,
            'height': height,
            'weight': weight,
            'volume': volume
        })

    postal_code = request.form['postal_code']
    companies = request.form.getlist('companies')

    # Fetch offers from database
    offers = Offer.query.filter(Offer.company_id.in_(companies)).all()

    results = []

    for offer in offers:
        if offer.min_weight <= total_weight <= offer.max_weight:
            if any(pc.postal_code == postal_code for pc in offer.postal_codes):
                cost = offer.base_cost
                if offer.extra_cost_per_kg is not None:
                    cost += (total_weight - offer.min_weight) * offer.extra_cost_per_kg
                if include_cubic_rate and total_volume:
                    cubic_cost = total_volume * offer.cubic_rate
                    cost = max(cost, cubic_cost)
                results.append({
                    'company': offer.company.name,
                    'cost': cost,
                    'error': None
                })

    if not results:
        results.append({
            'company': None,
            'cost': None,
            'error': 'No applicable offers found.'
        })

    return render_template('results.html', results=results)
    
@main_bp.route('/manage_postal_codes')
def manage_postal_codes():
    postal_codes = PostalCode.query.all()
    return render_template('manage_postal_codes.html', postal_codes=postal_codes)

@main_bp.route('/upload_postal_codes', methods=['GET', 'POST'])
def upload_postal_codes():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            try:
                process_csv(filepath)
                flash('File successfully uploaded and processed!')
            except Exception as e:
                flash(f'Error processing file: {e}')
            return redirect(url_for('main_bp.manage_postal_codes'))
    return render_template('upload_postal_codes.html')

def process_csv(filepath):
    with open(filepath, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            postal_code = row['postal_code']
            area_name = row['area_name']
            prefecture_name = row['prefecture_name']
            postal_code_entry = PostalCode(postal_code=postal_code, area_name=area_name, prefecture=prefecture_name)
            db.session.add(postal_code_entry)
        db.session.commit()

@main_bp.route('/get_location_data')
def get_location_data():
    postal_code = request.args.get('postal_code')
    results = db.session.query(
        PostalCode.area_name,
        PostalCode.prefecture_name
    ).filter(PostalCode.postal_code == postal_code).all()
    
    areas = [{'name': result[0]} for result in results]
    prefecture = results[0][1] if results else ''
    
    return jsonify({'areas': areas, 'prefecture': prefecture})

@main_bp.route('/add_postal_code', methods=['GET', 'POST'])
def add_postal_code():
    if request.method == 'POST':
        postal_code = request.form['postal_code']
        area_name = request.form['area_name']
        prefecture = request.form['prefecture']
        new_postal_code = PostalCode(postal_code=postal_code, area_name=area_name, prefecture=prefecture)
        db.session.add(new_postal_code)
        db.session.commit()
        flash('New postal code added successfully!')
        return redirect(url_for('main_bp.manage_postal_codes'))
    return render_template('add_postal_code.html')

@main_bp.route('/edit_postal_code/<int:id>', methods=['GET', 'POST'])
def edit_postal_code(id):
    postal_code = PostalCode.query.get_or_404(id)
    if request.method == 'POST':
        postal_code.postal_code = request.form['postal_code']
        postal_code.area_name = request.form['area_name']
        postal_code.prefecture = request.form['prefecture']
        db.session.commit()
        flash('Postal code updated successfully!')
        return redirect(url_for('main_bp.manage_postal_codes'))
    return render_template('edit_postal_code.html', postal_code=postal_code)

@main_bp.route('/search_postal_codes')
def search_postal_codes():
    query = request.args.get('query', '')
    if query:
        results = PostalCode.query.filter(PostalCode.postal_code.like(f'%{query}%')).all()
        return jsonify([{'postal_code': p.postal_code, 'area_name': p.area_name, 'prefecture': p.prefecture} for p in results])
    return jsonify([])
