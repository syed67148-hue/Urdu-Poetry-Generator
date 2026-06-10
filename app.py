from flask import Flask, render_template, request, jsonify

from generator import generate_poetry

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    category = data["category"]
    seed = data["seed"]

    category_map = {
        "romantic": "<ROMANTIC>",
        "sad": "<SAD>",
        "motivational": "<MOTIVATIONAL>",
        "islamic": "<ISLAMIC>",
        "story": "<STORY>"
    }

    prompt = f"{category_map.get(category,'')} {seed}"

    generated_text = generate_poetry(
        prompt,
        next_words=20
    )

    return jsonify({
        "output": generated_text
    })


if __name__ == "__main__":
    app.run(debug=True)