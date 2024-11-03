from flask import Flask, request, render_template

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def main():
    return render_template('welcome.html')

@app.route('/generate')
def generate():
    return render_template('index.html')

@app.route('/get_data',  methods=['POST'])
def get_data():
    data = request.get_json()
    if data:
        hotel_name = data.get('hotelName')
        pricePerNight = data.get('pricePerNight')
        category = data.get('category')
        services = data.get('services')
        features = data.get('features')

    print(data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
