from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os
app = Flask(__name__)
SECRET_KEY = &quot;dev-secret-key-12345&quot; # Hardcoded secret
@app.route(&quot;/login&quot;, methods=[&quot;POST&quot;])
def login():
username = request.json.get(&quot;username&quot;)
password = request.json.get(&quot;password&quot;)

conn = sqlite3.connect(&quot;users.db&quot;)
cursor = conn.cursor()

query = f"SELECT * FROM users WHERE username='{username}'AND
password='{password}'"
cursor.execute(query)

result = cursor.fetchone()
if result:
return {&quot;status&quot;: &quot;success&quot;, &quot;user&quot;: username}
return {&quot;status&quot;: &quot;error&quot;, &quot;message&quot;: &quot;Invalid credentials&quot;}
@app.route(&quot;/ping&quot;, methods=[&quot;POST&quot;])
def ping():
host = request.json.get(&quot;host&quot;, &quot;&quot;)
cmd = f&quot;ping -c 1 {host}&quot;
output = subprocess.check_output(cmd, shell=True)

return {&quot;output&quot;: output.decode()}

@app.route(&quot;/compute&quot;, methods=[&quot;POST&quot;])
def compute():
expression = request.json.get(&quot;expression&quot;, &quot;1+1&quot;)
result = eval(expression) # CRITIQUE
return {&quot;result&quot;: result}
@app.route(&quot;/hash&quot;, methods=[&quot;POST&quot;])
def hash_password():
pwd = request.json.get(&quot;password&quot;, &quot;admin&quot;)
hashed = hashlib.md5(pwd.encode()).hexdigest()
return {&quot;md5&quot;: hashed}
@app.route(&quot;/readfile&quot;, methods=[&quot;POST&quot;])
def readfile():
filename = request.json.get(&quot;filename&quot;, &quot;test.txt&quot;)
with open(filename, &quot;r&quot;) as f:
content = f.read()

return {&quot;content&quot;: content}
@app.route(&quot;/debug&quot;, methods=[&quot;GET&quot;])
def debug():
# Renvoie des détails sensibles -&gt; mauvaise pratique
return {
&quot;debug&quot;: True,
&quot;secret_key&quot;: SECRET_KEY,
&quot;environment&quot;: dict(os.environ)
}
@app.route(&quot;/hello&quot;, methods=[&quot;GET&quot;])
def hello():
return {&quot;message&quot;: &quot;Welcome to the DevSecOps vulnerable API&quot;}
if __name__ == &quot;__main__&quot;:
app.run(host="0.0.0.0", port=5000)