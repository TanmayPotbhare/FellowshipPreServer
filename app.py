from flask import Flask, render_template, make_response, request, redirect, session, url_for, jsonify, \
    flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FellowshipPreserver@123'


if __name__ == '__main__':
    app.run(debug = True)
