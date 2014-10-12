from flask import Flask, url_for

'''
simple test to show the url and their callbacks
'''

app = Flask(__name__)

@app.route('/')
def index():
    pass

@app.route('/main')
def main():
    pass

'''
test_request_context() method is used to mock an actual request
for testing purposes. Used in conjunction with the with statement, you
can activate the request to temporarily access session objects to test.
'''

with app.test_request_context():
    print('Route for index():', url_for('index'))
    print('Route for main():', url_for('main'))




