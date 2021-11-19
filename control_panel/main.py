import hashlib
from sqlite3 import IntegrityError

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from control_panel import create_app, db
from control_panel.forms import NewDeviceForm
from control_panel.models import Device
from tables import DeviceTable

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/devices/add', methods=['GET', 'POST'])
@login_required
def add_device():
    form = NewDeviceForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            h = hashlib.sha256()
            h.update(form.serial.data.encode('utf-8'))
            hashed_serial = h.hexdigest()
            created_device = Device(serial=form.serial.data,
                                    name=form.name.data,
                                    serial_hash=hashed_serial)
            db.session.add(created_device)
            try:
                db.session.commit()
                flash('Device added successfully.', category='success')
                return redirect(url_for('main.devices'))
            except IntegrityError:
                db.session.rollback()
                flash('Device with this serial number already exist.', category='error')
            return redirect(url_for('main.devices'))
        else:
            flash('Please fill empty fields.', category='warning')
    return render_template('device.html', form=form, header="Device registration")


@main.route('/devices/<device_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_device(device_id):
    device = Device.query.filter_by(id=device_id).first_or_404()
    if request.method == 'POST':
        form = NewDeviceForm()
        if form.validate_on_submit():
            device.name = form.name.data
            device.serial = form.serial.data
            h = hashlib.sha256()
            h.update(device.serial.encode('utf-8'))
            device.serial_hash = h.hexdigest()
            db.session.merge(device)
            try:
                db.session.commit()
                flash('Інформацію про пристрій успішно оновлено.', category='success')
                return redirect(url_for('main.devices'))
            except IntegrityError:
                db.session.rollback()
                flash('При оновленні інформації виникла помилка.', category='error')
            return redirect(url_for('main.devices'))
        else:
            flash('Інформацію про пристрій не оновлено, необхідні поля пусті.', category='warning')
    form = NewDeviceForm(device)
    return render_template('device.html', form=form, header="Edit device info")


@main.route('/devices', methods=['GET'])
@login_required
def devices():
    devices = Device.query.all()
    if len(devices) == 0:
        return render_template('devices.html',
                               table='<p class="subtitle is-italic has-text-dark has-text-centered" '
                                     'style="padding:20px;">'
                                     'Зареєстрованих пристроїв не знайдено</p>')
    table = DeviceTable(devices)
    return render_template('devices.html', table=table)


if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    app = create_app()

    app.run(debug=False, port=5001)
