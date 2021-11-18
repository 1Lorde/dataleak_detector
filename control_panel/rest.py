import hashlib
from flask import Blueprint, make_response
from .models import Device

rest = Blueprint('rest', __name__)


@rest.route("/devices/allowed", methods=['GET'])
def allowed_devices():
    devices = Device.query.all()

    hash = ''
    for dev in devices:
        hash += dev.serial_hash + ';'

    response = make_response(hash, 200)
    response.mimetype = "text/plain"
    return response


@rest.route("/devices/allowed/hash", methods=['GET'])
def allowed_devices_hash():
    allowed_devs = Device.query.all()

    hash = ''
    for dev in allowed_devs:
        hash += dev.serial_hash + ';'

    h = hashlib.sha256()
    h.update(hash.encode('utf-8'))

    response = make_response(h.hexdigest(), 200)
    response.mimetype = "text/plain"
    return response
