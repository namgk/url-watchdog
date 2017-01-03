import logging
import urllib2

from flask import Flask, render_template, request, jsonify
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb

app = Flask(__name__)

class Url(ndb.Model):
  status = ndb.StringProperty()
  url = ndb.StringProperty()

  @classmethod
  def get_by_url(cls, url):
    return cls.query().filter(cls.url == url).get()

class UrlBackend():
  def getUrls(self):
    urls = Url.query().fetch()
    return [{"url": u.url, "status": u.status} for u in urls]

  def addUrl(self,u):
    url = Url(status='unknown', url=u, id=u)
    url.put()
    return {"added_url": url.url}

  def delUrl(self,u):
    url = Url.get_by_url(u)
    if url is not None:
      url.key.delete()
    return {"deleted_url": u}

urlBackend = UrlBackend()


@app.route('/api/urls', methods=['GET'])
def getUrls():
  res = urlBackend.getUrls()
  return jsonify(res)

@app.route('/api/url', methods=['POST'])
def postUrl():
  url = request.json['u']
  if not url:
      return 'url must be present', 400

  res = urlBackend.addUrl(url)
  return jsonify(res)

@app.route('/api/url/<url>', methods=['DELETE'])
def deleteUrl(url):
  if not url:
      return 'url must be present', 400

  url = url.replace(':','%3A')
  res = urlBackend.delUrl(url)
  return jsonify(res)

@app.route('/cron')
def cron():
  urls = urlBackend.getUrls()
  for url in urls:
    storedUrl = Url.get_by_url(url['url'])
    urlStr = urllib2.unquote(url['url']).decode('utf8')
    try:
      res = urllib2.urlopen(urlStr, timeout = 10)
      assert res.getcode() == 200
      storedUrl.status = 'ok'
    except Exception as err:
      if storedUrl.status != 'failed':
        storedUrl.status = 'failed'
        mail.send_mail(
          sender="giangnam.bkdtvt@gmail.com",
          to="Nam Giang <giangnam.bkdtvt@gmail.com>",
          subject="Server down: {}".format(urlStr),
          body="{} is down!".format(urlStr))
    storedUrl.put()
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