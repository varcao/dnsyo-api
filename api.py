from flask import Flask
from dnsyo import dnsyo
import json

app = Flask(__name__)

@app.route('/')
def info():
  return "TODO: show some info here"

@app.route('/<domain>')
def query(domain):

  lookup = dnsyo.lookup(
      domain=str(domain),
      recordType="A",
      listLocation="https://raw.github.com/samarudge/dnsyo/master/resolver-list.yml",
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