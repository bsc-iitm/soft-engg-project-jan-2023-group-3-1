from flask_security import (
        RegisterForm,
        unique_identity_attribute,
    )
from wtforms import validators, SelectField

choices = {
            'Student':'student',\
            'Support Staff':'support staff',\
            'Admin':'admin'
        }
class Registerform_roles(RegisterForm):
    role = SelectField(label="Role",\
                        validators=[
                            validators.data_required(),
                            unique_identity_attribute
                        ],\
                        choices=['Student','Support Staff','Admin']
                    )