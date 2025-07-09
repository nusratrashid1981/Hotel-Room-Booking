from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'


# Discounts
discounts = {
    'BR004': 0.1,
    'BR005': 0.15,
    'BR006': 0
}

# Max nights
max_nights = 30


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            room_type = request.form['room_type']
            num_nights = int(request.form['num_nights'])

            if not room_type or not num_nights:
                flash('Please fill in all fields.', 'error')
            elif num_nights > max_nights:
                flash(f'Maximum {max_nights} nights allowed.', 'error')
            else:
                total_cost = calculate_cost(room_type, num_nights)
                return redirect(url_for('result', total_cost=total_cost))

        except ValueError:
            flash('Please enter a valid number of nights.', 'error')

    return render_template('index.html')


def calculate_cost(room_type, num_nights):
    base_prices = {
        'BR001': 100,
        'BR002': 150,
        'BR003': 200
    }

    base_price = base_prices.get(room_type, 0)
    discount = 0

    for discount_key, discount_value in discounts.items():
        if num_nights >= int(discount_key[2:]):
            discount = discount_value

    if num_nights >= 7:
        discount = discounts['BR005']
    elif num_nights >= 3:
        discount = discounts['BR004']

    total_cost = base_price * num_nights * (1 - discount)
    return total_cost


@app.route('/result/<float:total_cost>')
def result(total_cost):
    return render_template('result.html', total_cost=total_cost)


if __name__ == '__main__':
    app.run(debug=True)
