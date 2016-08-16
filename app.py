from flask import Flask
import apic

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, IMAPEX!'

@app.route('/ticket/')
def check_ticket():
    return apic.get_ticket()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
