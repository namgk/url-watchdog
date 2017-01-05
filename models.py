from google.appengine.ext import ndb

class Url(ndb.Model):
  status = ndb.StringProperty()
  url = ndb.StringProperty()
