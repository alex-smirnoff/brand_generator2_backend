from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import csv

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://alex-smirnoff.github.io"}})


@app.route('/')
def stats_panel():

    with open('/home/alexsmirnoff98/mysite/total_stats.txt', 'r') as file:
        lines = file.readlines()
        visits = re.search(r'\d+', lines[0]).group(0)
        cards = re.search(r'\d+', lines[1]).group(0)
        signatures = re.search(r'\d+', lines[2]).group(0)

    assets_dict = {}

    with open('/home/alexsmirnoff98/mysite/products_by_assets.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if row[1] in assets_dict:
                products = [i for i, _ in assets_dict[row[1]]]
                if row[0] in products:
                    for i2, (existing_product, count) in enumerate(assets_dict[row[1]]):
                        if existing_product == row[0]:
                            assets_dict[row[1]][i2] = (existing_product, count + 1)
                            break
                else:
                    assets_dict[row[1]].append((row[0], 1))
            else:
               assets_dict[row[1]] = [(row[0], 1)]

    for asset, products in assets_dict.items():
        print(f"{asset}: {products}")

    web_page_panel = """

    <!DOCTYPE html>
    <html>
    <header>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>In.Spire Stats</title>
        <style>
            .cards {
              position: relative;
              display: flex;
              gap: 15px;
              align-items:center;
              justify-content:center;
              font-family:arial;
            }

            .cards .red {
              background-color: #f43f5e;
            }

            .cards .blue {
              background-color: #3b82f6;
            }

            .cards .green {
              background-color: #22c55e;
            }

            .cards .card {
              display: flex;
              align-items: center;
              justify-content: center;
              flex-direction: column;
              text-align: center;
              height: 100px;
              width: 250px;
              border-radius: 10px;
              color: white;
              cursor: pointer;
              transition: 400ms;
            }

            .cards .card p.tip {
              font-size: 1em;
              font-weight: 700;
            }

            .cards .card p.second-text {
              font-size: .7em;
            }

            .cards .card:hover, .graph-element:hover{
              transform: scale(1.1, 1.1);
            }

            .cards:hover > .card:not(:hover), .horizontal-graph:hover > .graph-element:not(:hover) {
              transform: scale(0.9, 0.9);
            }

            .devider{
              height: 50px;
              width: 100%;
            }

            .container {
              width: 60%;
              max-width: 360px;
              height: auto;
              position: relative;
            }

            .horizontal-graph, .graph-element{
              cursor: pointer;
              transition: 400ms;
            }

            .horizontal-graph:first-child {
            }

            .graph-container {
              overflow: hidden;
              background-color: #eee;
              border-radius: 2px;
            }

            .graph-bar {
              height: 14px;
              background: #ff6c0c;
              border-top-right-radius: 2px;
              border-bottom-right-radius: 2px;
              opacity: 0;
              animation: 1s anim-lightspeed-in ease forwards;
            }

            @keyframes anim-lightspeed-in {
              0% {transform: translateX(-200%); opacity: 1;}
              100% {transform: translateX(0);  opacity: 1;}
            }
        </style>
    </header>
    <body style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <p style="font-family: arial; font-size: 20px;">Загальна статистика щодо сервісу In.Spire<p>
        <div class="cards">
            <div class="card red">
                <p class="tip">""" + str(visits) + """</p>
                <p class="second-text">Відвідування сторінки</p>
            </div>
            <div class="card blue">
                <p class="tip">""" + str(cards) + """</p>
                <p class="second-text">Всього створено візиток</p>
            </div>
            <div class="card green">
                <p class="tip">""" + str(signatures) + """</p>
                <p class="second-text">Всього створено підписів</p>
            </div>
        </div>
        <div class="devider" style="position: relative;"></div>
        <div class="titles_div" style="position: relative; display: flex; justify-content: space-evenly; min-width: 775px; height: auto;">
            <div class="titles_box1" style="max-width: 49%; height: auto;"><p style="font-family: arial; font-size: 15px;">Створено візиток за активами</p></div>
            <div class="titles_box2" style="max-width: 49%; height: auto;"><p style="font-family: arial; font-size: 15px;">Створено підписів за активами</p></div>
        </div>
        <div class="container_div" style="position: relative; display: flex; justify-content: space-between; align-content: start; min-width: 775px; height: auto;">
            <div class="container" style="display: flex; flex-direction: column; align-items: flex-start;">
                <div class="horizontal-graph graph-ani" style="min-width: 360px;display: flex; flex-direction:column; align-content: start;">

    """


    card_count_list = [(asset, sum(count for product, count in products if product == 'card')) for asset, products in assets_dict.items()]
    sorted_card_count = sorted(card_count_list, key=lambda x: x[1], reverse=True)
    sorted_data_card = {asset: products for asset, products in sorted_card_count}


    for asset, products in sorted_data_card.items():
        if products > 0:
            web_page_panel += """
                        <div class="graph-element" style="width: 100%; height:auto;">
                            <p style="font-family:arial; font-size: 15px; color: grey;">""" + asset + """</p>
                            <div class="graph-container" style="margin: 0px;">
                                <div class="graph-bar" style="display: flex; justify-content: right; width: """ + str(int(products) / int(cards) * 100) +"""%;">
                                    <p style="font-family:arial; font-size: 10px; color: white; align-self: center; padding-right: 10px;">""" + str(products) + """</p>
                                </div>
                            </div>
                        </div>

    """

    web_page_panel += """
                </div>
            </div>
            <div class="container" style="min-width: 360px;display: block;">
                <div class="horizontal-graph graph-ani" style="display: block;">

   """

    signature_count_list = [(asset, sum(count for product, count in products if product == 'signature')) for asset, products in assets_dict.items()]
    sorted_signature_count = sorted(signature_count_list, key=lambda x: x[1], reverse=True)
    sorted_data_signature = {asset: products for asset, products in sorted_signature_count}

    for asset, products in sorted_data_signature.items():
        if products > 0:
            web_page_panel += """
                        <div class="graph-element" style="width: 100%; height:auto;">
                            <p style="font-family:arial; font-size: 15px; color: grey;">""" + asset + """</p>
                            <div class="graph-container" style="margin: 0px;">
                                <div class="graph-bar" style="display: flex; justify-content: right; width: """ + str(int(products) / int(cards) * 100) +"""%;">
                                    <p style="font-family:arial; font-size: 10px; color: white; align-self: center; padding-right: 10px;">""" + str(products) + """</p>
                                </div>
                            </div>
                        </div>

    """

    web_page_panel += """
                </div>
            </div>
        </div>
    </body>
    </html>

   """

    return web_page_panel

@app.route('/api/receive_xhr', methods=['POST'])
def receive_xhr():
    data = request.json

    if "visit" in data:
        with open('/home/alexsmirnoff98/mysite/total_stats.txt', 'r') as file:
            lines = file.readlines()
            lines[0] = re.sub(r'\d+', lambda x: str(int(x.group()) + 1), lines[0])
        with open('/home/alexsmirnoff98/mysite/total_stats.txt', 'w') as file:
            file.writelines(lines)
        with open('/home/alexsmirnoff98/mysite/attendance_by_time.txt', 'a') as file:
            file.write(data["date"] + "\n")

    if "product" in data:
        if data["product"] == "card":
            with open('/home/alexsmirnoff98/mysite/total_stats.txt', 'r') as file:
                lines = file.readlines()
                lines[1] = re.sub(r'\d+', lambda x: str(int(x.group()) + 1), lines[1])
            with open('/home/alexsmirnoff98/mysite/total_stats.txt', 'w') as file:
                file.writelines(lines)
            with open('/home/alexsmirnoff98/mysite/products_by_assets.csv', 'a') as file:
                file.write("\n" + data["product"] + "," + data["asset"])
        elif data["product"] == "signature":
            with open('/home/alexsmirnoff98/mysite/total_stats.txt', 'r') as file:
                lines = file.readlines()
                lines[2] = re.sub(r'\d+', lambda x: str(int(x.group()) + 1), lines[2])
            with open('/home/alexsmirnoff98/mysite/total_stats.txt', 'w') as file:
                file.writelines(lines)
            with open('/home/alexsmirnoff98/mysite/products_by_assets.csv', 'a') as file:
                file.write("\n" +  data["product"] + "," + data["asset"])

    response_data = {'message': 'XHR request received and processed', 'data': data}
    response = jsonify(response_data)
    response.headers.add('Access-Control-Allow-Origin', 'https://alex-smirnoff.github.io')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')

    return response