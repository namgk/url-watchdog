import logging
import urllib2

from flask import Flask, render_template, request
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb

app = Flask(__name__)

class Host(ndb.Model):
  name = ndb.StringProperty()
  url = ndb.StringProperty()


@app.route('/host/<hostName>', methods=['DELETE', 'GET'])
def processHostDelete(hostName):
  if request.method == 'DELETE':
    return 'ok'
  elif request.method == 'GET':
    h = ndb.Key('Host', hostName).get()
    if h:
      res = h.url
    else:
      res = 'not found'
    return res

@app.route('/host', methods=['POST'])
def processHost():
  name = request.json['name']
  url = request.json['url']

  if not name or not url:
    return 'name and url must be present', 400

  host = Host(name=name, url=url, id=name)
  host.put()
  return 'ok'

@app.route('/cron')
def cron():
  query = Host.query()
  print(query.fetch())
  return 'ok'

@app.route('/urlcheck')
def urlcheck():
  url = request.args.get('url')
  try:
    res = urllib2.urlopen(url, timeout = 10)
    assert res.getcode() == 200
    return 'ok'
  except Exception as err:
    mail.send_mail(
      sender="giangnam.bkdtvt@gmail.com",
      to="Nam Giang <giangnam.bkdtvt@gmail.com>",
      subject="Server down: {}".format(url),
      body="{} is down!".format(url))
    return "error: {0}".format(err)

@app.route('/admin')
def admin():
  user = users.get_current_user()
  if user:
    nickname = user.nickname()
    logout_url = users.create_logout_url('/')
    greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
        nickname, logout_url)
  else:
    login_url = users.create_login_url('/')
    greeting = 'Please sign in! (<a href="{}">sign in</a>)'.format(login_url)
  return render_template(
    'test.html',
    greeting=greeting, urls = Host.query().fetch())

@app.route('/form')
def form():
  return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
  name = request.form['name']
  email = request.form['email']
  site = request.form['site_url']
  comments = request.form['comments']
  return render_template(
    'submitted_form.html',
    name=name,
    email=email,
    site=site,
    comments=comments)

@app.route('/')
def hello():
  return render_template(
    'index.html')


@app.errorhandler(500)
def server_error(e):
  # Log the error and stacktrace.
  logging.exception('An error occurred during a request.')
  return 'An internal error occurred.', 500

if __name__ == "__main__":
  app.run()