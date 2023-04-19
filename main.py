# Project is going to be a basic website that pulls information to make a web api request
# will grab from daily quote

from flask import Flask, render_template, request
import requests
app = Flask(__name__)


def getMotivated():
    # parameters = {
    #     "amount": 10,
    #     "type": "boolean",
    # }

    # response = requests.get("https://opentdb.com/api.php", params=parameters)
    response = requests.get("https://zenquotes.io/api/today")
    response.raise_for_status()
    data = response.json()
    # quote = data[0]
    quote = data
    return quote
    # print(quotes)
    # pass

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # f = request.files['file']
        # colour_code = request.form['colour_code']
        # hexes = give_most_hex(f.stream, colour_code)
        # return render_template('index.html', colors_list=hexes, code=colour_code)
        quote = getMotivated()
        # return render_template('index.html', quote=quote['q'],author=quote['a'])
        # print(quote)
        # print(quote["h"])
        return render_template('index.html', quoteJSON=quote)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)