from flask import Flask, render_template, request, jsonify

from ice_breaker import ice_break

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    person_intel, profile_pic_url = ice_break(name=name)
    print(profile_pic_url) #here there is a valid url for the profile pic
    return jsonify(
        {
            "summary": person_intel.summary,
            "facts": person_intel.facts,
            "interests": person_intel.topics_of_interest,
            "ice_breakers": person_intel.ice_breakers,
            "profile_pic_url": profile_pic_url,

        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
