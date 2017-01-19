from google.appengine.ext import ndb

class Url(ndb.Model):
  status = ndb.StringProperty()
  url = ndb.StringProperty()
  attempt = ndb.IntegerProperty()

  def sync(self, url_dict):
    if 'status' in url_dict:
      self.status = url_dict['status']
    if 'url' in url_dict:
      self.url = url_dict['url']
    if 'attempt' in url_dict:
      self.attempt = url_dict['attempt']
