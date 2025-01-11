from datetime import date

import requests
from flask import Flask, render_template, request

app = Flask(__name__)


product_list = [{
        'id': '1',
        'title': 'Dior for Man',
        'price': '59',
        'description': 'Founded in 1946, the House of Dior made its first foray into the fragrance field with Miss '
                       'Dior. A green, chypre scent.'
        ,
        'image': '../static/productImg/lastpro1.jpg'
    },
        {
            'id': '2',
            'title': 'Dior for Woman',
            'price': '69',
            'description': 'Founded in 1946, the House of Dior made its first foray into the fragrance field with Miss '
                           'Dior. A green, chypre scent.',
            'image': '../static/productImg/lastpro2.jpg'
        }
    ]


@app.get('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/jinja')
def jinja():
    return render_template('jinja.html')


@app.route('/product')
def product():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    product = response.json()
    product_list = product
    return render_template('Product.html', product_list=product_list)


@app.route('/product_detail')
def product_detail():
    product_id = request.args.get('id')
    # current_product = []
    # for item in product_list:
    #     if item['id'] == product_id:
    #         current_product = item
    # return f"{product_id}"
    url = "https://fakestoreapi.com/products/{}".format(product_id)
    response = requests.get(url)
    current_product = []
    current_product = response.json()
    return render_template("product_detail.html ", current_product=current_product)


@app.get('/checkout')
def checkout():
    product_id = request.args.get('id')
    url = "https://fakestoreapi.com/products/{}".format(product_id)
    response = requests.get(url)

    current_product = response.json()
    # current_product = []
    # for item in product_list:
    #     if item['id'] == product_id:
    #         current_product = item
    # return f"{product_id}"
    return render_template("checkout.html ", current_product=current_product)


@app.post('/submit_order')
def submit_order():
    product_id = request.form.get('product_id')
    # current_product = []
    # for item in product_list:
    #     if item['id'] == product_id:
    #         current_product = item
    #
    name = request.form.get('fullname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    # # return 'submit_order'
    # return current_product
    url = f"https://fakestoreapi.com/products/{product_id}"
    response = requests.get(url)
    current_product = response.json()
    html = (
        "<strong🤴 >{name}</strong>\n"
        "<strong>🙆️ {phone}</strong>\n"
        "<code>🛌 {email}</code>\n"
        "<code>============================</code>\n"
        "<strong>🧾 {inv_no}</strong>\n"
        "<code>📆 {date}</code>\n"
        "<code>============================</code>\n"
        "<code>ID\t\tQuality\t\tPrice\t\tAmount</code>\n"
    ).format(
        inv_no='INV0001',
        date=date.today(),
        name=f"{name}",
        phone=f"{phone}",
        email=f"{email}"

    )
    html += (
        f"<code>{current_product['id']}\t\t\t\t\t\t1\t\t\t\t\t{current_product['price']}\t\t\t\t{current_product['price']}</code>\n "
    )
    html += (
        "<code>-----------------------------</code>\n"
        "<code>Total: {total}$</code>\n"
        "<code>Grand Total: {grand_total}$</code>\n"

    ).format(
        total=f'{current_product["price"]}',
        grand_total=f'{current_product["price"]}',
    )

    bot_token = "6847809785:AAFWbjBKRafyarq3sI_ddvP3lPBp2kfqeaA"
    chat_id = "@pharanotify_channel"

    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    product = response.json()
    product_list = product

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    # Replace 'image_path' with the path to the image you want to send.
    image_path = current_product['image']
    # res = requests.get(
    #     f"https://api.telegram.org/bot7122074711:AAFcEsKdu_q4-ZpOAywcuQRRbk7quHvJAbo/sendMessage?chat_id=@theara_st34&text={html}&parse_mode=HTML")
    # res = requests.post(url, files=files, data=data)

    res = requests.get("https://api.telegram.org/bot{}/sendPhoto".format(bot_token),
                       params=
                       {
                           'chat_id': chat_id,
                           'photo': image_path,
                           'caption': html,
                           'parse_mode': 'HTML'
                       })

    # return response.status_code
    return render_template("ordered.html", current_product=current_product)


@app.route('/num')
def number_format():
    num = 1234567.8910
    formatted_num = format(num, ',')  # Adds comma as thousand separator
    return f'Formatted number: {formatted_num}'


if __name__ == '__main__':
    app.run()
