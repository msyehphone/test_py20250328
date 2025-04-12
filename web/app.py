from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

@app.route("/", methods=["GET", "POST"])
def index():
    definitions = []
    error = None
    if request.method == "POST":
        word = request.form.get("word")
        if word:
            response = requests.get(f"{API_URL}{word}")
            if response.status_code == 200:
                data = response.json()
                try:
                    meanings = data[0]["meanings"]
                    for meaning in meanings:
                        for definition in meaning["definitions"]:
                            definitions.append(definition["definition"])
                except (KeyError, IndexError):
                    error = "Unexpected response format. Please try another word."
            else:
                error = "Word not found. Please try another."
    return render_template("index.html", definitions=definitions, error=error)

if __name__ == "__main__":
    app.run(debug=True)
