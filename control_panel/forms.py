from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NewDeviceForm(FlaskForm):
    name = StringField("Name")
    serial = StringField("Serial number", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, device=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if device:
            self.name.data = device.name
            self.serial.data = device.serial
