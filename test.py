from flask import jsonify, render_template, request
import json
import threading
import time


data_file = open("/home/dimitri/ETH/workspace/webproject1/app/turn.json")    
data = json.load(data_file)

