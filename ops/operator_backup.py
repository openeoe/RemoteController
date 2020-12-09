# -*- coding: utf-8 -*-
import os
import sys
import requests
import yaml
import tarfile
import json
import io
import sys
import config as cp
from importlib import reload
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/<int:num>')
def inputTest(num=None):
    return render_template('main.html', num=num)

@app.route('/johab', methods=['GET'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('johab.html', colours=colours)

@app.route('/calculate',methods=['POST'])
def calculate(num=None):
    if request.method == 'POST':
        temp = request.form['num']
    else:
        temp = None
    return redirect(url_for('inputTest',num=temp))

# node list 가져오는 함수 구현
def



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
