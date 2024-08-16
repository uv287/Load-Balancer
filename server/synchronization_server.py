from flask import Flask
app = Flask(__name__)

@app.route('/sync')
def sync():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)