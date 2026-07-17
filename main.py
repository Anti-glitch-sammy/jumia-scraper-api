from bs4 import BeautifulSoup
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the web scraping api!"

@app.route('/specs', methods=['POST'])
def specs():
    link = request.args.get('url')
    if not link:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    response = requests.get(link)
    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch page, status {response.status_code}"}), 502

    soup = BeautifulSoup(response.text, 'html.parser')
    specs = [[spec.find('h3'), spec.find_all('li') or spec.find_all('p')] for spec in soup.find_all('div', class_='card-b -fh')]
    final_specs = {}

    for spec in specs:
        if spec[0] is None:
            continue
        final_specs[spec[0].text] = [li.text for li in spec[1]]

    return jsonify(final_specs)


if __name__ == '__main__':
    app.run(debug=True)