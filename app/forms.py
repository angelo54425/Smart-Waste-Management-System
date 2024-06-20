from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    names = StringField("Names", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    address = StringField("Address", validators=[DataRequired()])
    role = SelectField(
        "Role",
        choices=[
            ("house-hold", "House Hold"),
            ("service-man", "Service Man"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ScheduleForm(FlaskForm):
    day_of_week = SelectField(
        "Choose a Day of the Week",
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Add Schedule")


class GenerateCollectionsForm(FlaskForm):
    submit = SubmitField("Generate Upcoming Collections")


class CollectionForm(FlaskForm):
    material = StringField("Material", validators=[DataRequired()])
    quantity = FloatField("Quantity", validators=[DataRequired()])
    waste_category = StringField("Waste Category", validators=[DataRequired()])
    submit = SubmitField("Submit")
