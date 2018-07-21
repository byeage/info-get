from flask import Flask
from flask import render_template, request, jsonify
import json
import requests
app = Flask(__name__)

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        res = request.get_json()
        url = res['url']
        headers = res['header']
        cookies = res['cookie']
        html = requests.get(url, headers=headers, cookies = cookies)
        print(json.dumps(headers))
        print(json.dumps(cookies))
        print(html.content)
        return jsonify(res)
    else:
        return 'posts'

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)





if __name__ == '__main__':
    app.debug = True
    app.run()
