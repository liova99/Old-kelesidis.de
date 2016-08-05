from flask import render_template, Blueprint, flash, request, redirect
from flask_wtf import Form
from wtforms import (StringField, BooleanField, TextAreaField, SubmitField,
                     validators, ValidationError)
from flask_mail import Mail, Message

from time import sleep
from app import mail



contact_blueprint = Blueprint("contact", __name__)
contact_success_blueprint = Blueprint("contact_success", __name__)

@contact_blueprint.route("/contact/", methods = ["GET", "POST"])
def contact():
    title = "Contact"
    form = contact_form()

    if request.method == "POST":
        if form.validate() == False:
            flash("All fields are required.")
            return render_template("contact.html",form = form, title = title)

        else:
            msg = Message(form.name.data, sender = 'levan@kelesidis.de', recipients = ['levan@kelesidis.de'] )
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('contact_success.html')

    elif request.method == "GET":
        return render_template("contact.html", form=form, title = title)

@contact_success_blueprint.route("/contact_success/")
def contact_success():
    title = "Message sent"

    return render_template("contact_success.html", title = title)


class contact_form(Form):
    name = StringField("Name", [validators.Required("Please enter your name.")])
    email = StringField("Email", [validators.Required("Please enter your email address."), validators.Email()])
    message = TextAreaField("Message", [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")


