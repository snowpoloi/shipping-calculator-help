from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Company, Offer, PostalCode, OfferPostalCode

offer_bp = Blueprint('offer_bp', __name__, url_prefix='/offers')

@offer_bp.route('/offers', methods=['GET'])
def offers():
    offers = Offer.query.all()
    companies = Company.query.all()
    return render_template('offers.html', companies=companies, offers=offers)

@offer_bp.route('/add_offer', methods=['GET', 'POST'])
def add_offer():
    if request.method == 'POST':
        company_id = request.form['company_id']
        offer_type = request.form['offer_type']
        min_weight = float(request.form['min_weight']) if request.form['min_weight'] else None
        max_weight = float(request.form['max_weight']) if request.form['max_weight'] else None
        base_cost = float(request.form['base_cost'])
        extra_cost_per_kg = float(request.form['extra_cost_per_kg']) if request.form['extra_cost_per_kg'] else None
        cubic_rate = float(request.form['cubic_rate']) if request.form['cubic_rate'] else None
        min_charge = float(request.form['min_charge']) if request.form['min_charge'] else None

        new_offer = Offer(
            company_id=company_id,
            offer_type=offer_type,
            min_weight=min_weight,
            max_weight=max_weight,
            base_cost=base_cost,
            extra_cost_per_kg=extra_cost_per_kg,
            cubic_rate=cubic_rate,
            min_charge=min_charge
        )
        db.session.add(new_offer)
        db.session.commit()

        selected_postal_codes = request.form['selected_postal_codes'].split(',')
        for postal_code_id in selected_postal_codes:
            offer_postal_code = OfferPostalCode(
                offer_id=new_offer.id,
                postal_code_id=int(postal_code_id)
            )
            db.session.add(offer_postal_code)

        db.session.commit()
        flash('Offer added successfully!')
        return redirect(url_for('offer_bp.offers'))

    companies = Company.query.all()
    postal_codes = PostalCode.query.all()

    postal_codes_dict = [{'id': pc.id, 'postal_code': pc.postal_code, 'area_name': pc.area_name, 'prefecture': pc.prefecture} for pc in postal_codes]

    return render_template('add_offer.html', companies=companies, postal_codes=postal_codes_dict)

@offer_bp.route('/offers/edit_offer/<int:id>', methods=['GET', 'POST'])
def edit_offer(id):
    offer = Offer.query.get_or_404(id)
    companies = Company.query.all()
    postal_codes = PostalCode.query.all()

    if request.method == 'POST':
        form = OfferForm(request.form)
        if form.validate():
            offer.company_id = form.company_id.data
            offer.offer_type = form.offer_type.data
            offer.min_weight = form.min_weight.data
            offer.max_weight = form.max_weight.data
            offer.base_cost = form.base_cost.data
            offer.extra_cost_per_kg = form.extra_cost_per_kg.data
            offer.cubic_rate = form.cubic_rate.data
            offer.min_charge = form.min_charge.data

            selected_postal_codes = request.form.getlist('selected_postal_codes')
            offer.postal_codes = [OfferPostalCode(offer_id=offer.id, postal_code_id=pc_id) for pc_id in selected_postal_codes]

            db.session.commit()
            flash('Offer updated successfully', 'success')
            return redirect(url_for('offer_bp.view_offers'))
        else:
            flash('Error updating offer', 'danger')

    selected_postal_codes = [pc.postal_code_id for pc in offer.postal_codes]
    return render_template('edit_offer.html', offer=offer, companies=companies, postal_codes=postal_codes, selected_postal_codes=selected_postal_codes)


@offer_bp.route('/offers/delete_offer/<int:offer_id>', methods=['POST'])
def delete_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    db.session.delete(offer)
    db.session.commit()
    return redirect(url_for('offer_bp.offers'))