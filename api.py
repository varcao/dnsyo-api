from flask import Flask
from flask import request
from flask import render_template
from dnsyo import dnsyo
import json

app = Flask(__name__)

@app.route('/')
def info():
  return render_template("index.html")

@app.route('/resolver', methods=['POST'])
def query():

  domain = request.form.get("domain")
  lookup = dnsyo.lookup(
      domain=str(domain),
      recordType="A",
      listLocation="https://raw.githubusercontent.com/varcao/dnsyo-api/master/resolver-list.yml",
      maxWorkers=100,
      maxServers=500
  )

  lookup.query(
    progress=False
  )

  successfulResponses = len([True for rsp in lookup.results if rsp['success']])

  out = {
    'domain': str(domain),
    'successfulResponses': successfulResponses,
    'totalQueried': len(lookup.serverList),
    'errorResponses': len(lookup.serverList) - successfulResponses
  }

  return json.dumps(out)


if __name__ == '__main__':
  app.run(debug=True)
