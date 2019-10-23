# http://localhost:5000/listarhw
import subprocess
from flask import Flask, request, jsonify,json, session, redirect, url_for, escape


app = Flask(__name__)
app.config['SECRET_KEY'] = "ADM-hwPC"

command = ('lshw -json')

p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

text = p.stdout.read()
retcode = p.wait()
print(text)

new_text = json.loads(text)


@app.route('/listarhw', methods= ['GET'])
def home():
    return  jsonify(new_text), 200

if __name__ == '__main__':
    app.run(debug=True)








"""import subprocess

command = ('lshw')

p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
text = p.stdout.read()
retcode = p.wait()
print(text)
print(type(text))"""



"""import os  # seu sistema operacional
from elevate import elevate
from flask import Flask, request, jsonify

app = Flask(__name__)

def is_root():
    return os.getuid() == 0
print("ROOT? ", is_root())
elevate()
os.system("lshw")
#lista = os.system("lshw -json")
print(os.system("lshw -html"))

@app.route('/lista', methods=['GET'])
def home():
    return jsonify(os.system("lshw")), 200

if __name__ == '__main__':
    app.run(debug=True)

"""
"""
import json
import os  # seu sistema operacional
import subprocess  # comandos do sistema
import sys
from elevate import elevate

def is_root():
    return os.getuid() == 0
print("ROOT? ", is_root())
elevate()
#print("ROOT? ", is_root())
os.system("lshw")
#var = subprocess.getoutput("lshw")  # pega a saida
#print(var)

#print(type(os.system("lshw -html")))
print(os.system("lshw -json"))
"""
