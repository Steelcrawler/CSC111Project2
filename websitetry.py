import os

from flask import Flask, render_template, request

selected_values = {}

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/result', methods=['POST'])
def result():
    global selected_values

    selected_options = [request.form.get(f'dropdown_{i + 1}') for i in range(7)]

    # Store selected dropdown values in the dictionary
    for i, option in enumerate(selected_options):
        selected_values[f'dropdown_{i + 1}'] = option

    return f"You selected: {', '.join(selected_options)}"


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 3455)))
