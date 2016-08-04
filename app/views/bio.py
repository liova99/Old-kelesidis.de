from flask import render_template, Blueprint


bio_blueprint = Blueprint("bio", __name__)


@bio_blueprint.route("/bio/")
def bio():
    title = "Kelesidis Levan Bio"

    return render_template("bio.html", title = title)