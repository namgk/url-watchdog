import logging
import urllib2

from flask import Flask, render_template, request, jsonify
from google.appengine.api import users
from google.appengine.api import mail


from backend import Backend, BackendResult

app = Flask(__name__)

# class Url(ndb.Model):
#   status = ndb.StringProperty()
#   url = ndb.StringProperty()

#   @classmethod
#   def get_by_url(cls, url):
#     return cls.query().filter(cls.url == url).get()

# class UrlBackend():
#   def getUrls(self):
#     urls = Url.query().fetch()
#     return [u.to_dict() for u in urls]

#   def addUrl(self,u):
#     url = Url(status=u['status'], url=u['url'])
#     url.put()
#     newUrl = url.to_dict()
#     newUrl['id'] = url.key.id()
#     return newUrl

#   def delUrl(self,uid):
#     url = Url.get_by_id(uid)
#     if url is None:
#       return {'error': 'key not found'}

#     url.key.delete()
#     return url.to_dict()

urlBackend = Backend()

@app.route('/api/urls', methods=['GET'])
def getUrls():
  res = urlBackend.getUrls()
  if res.ok:
    return jsonify(res.result)
  else:
    return res.result, 400

@app.route('/api/url', methods=['POST'])
def addUrl():
  url = request.json
  if not url:
      return 'url must be present', 400

  res = urlBackend.addUrl(url)
  if res.ok:
    return jsonify(res.result)
  else:
    return res.result, 400

@app.route('/api/url/<uid>', methods=['DELETE'])
def deleteUrl(uid):
  if not uid:
      return 'url id must be present', 400

  res = urlBackend.deleteUrl(long(uid))
  if res.ok:
    return jsonify(res.result)
  else:
    return res.result, 400

@app.route('/cron')
def cron():
  res = urlBackend.getUrls()
  if not res.ok:
    return 'error fetching data', 400

  for url in res.result:
    try:
      res = urllib2.urlopen(url['url'], timeout = 10)
      assert res.getcode() == 200
      url['status'] = 'ok'
    except Exception as err:
      if url['status'] != 'failed':
        url['status'] = 'failed'
        mail.send_mail(
          sender="giangnam.bkdtvt@gmail.com",
          to="Nam Giang <giangnam.bkdtvt@gmail.com>",
          subject="Server down: {}".format(urlStr),
          body="{} is down!".format(urlStr))
    urlBackend.update(url)
  return 'ok'

# @app.route('/urlcheck')
# def urlcheck():
#   url = request.args.get('url')
#   try:
#     res = urllib2.urlopen(url, timeout = 10)
#     assert res.getcode() == 200
#     return 'ok'
#   except Exception as err:
#     mail.send_mail(
#       sender="giangnam.bkdtvt@gmail.com",
#       to="Nam Giang <giangnam.bkdtvt@gmail.com>",
#       subject="Server down: {}".format(url),
#       body="{} is down!".format(url))
#     return "error: {0}".format(err)

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
    'admin.html',
    greeting=greeting)

# @app.route('/')
# def hello():
#   return render_template(
#     'index.html')

@app.errorhandler(500)
def server_error(e):
  # Log the error and stacktrace.
  logging.exception('An error occurred during a request.')
  return 'An internal error occurred.', 500

if __name__ == "__main__":
  app.run()