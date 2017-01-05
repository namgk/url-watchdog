from google.appengine.ext import ndb
from models import Url

def to_dict(ndbObject):
  d = ndbObject.to_dict()
  d['id'] = ndbObject.key.id()
  return d

class Backend():

  def getUrls(self):
    return BackendResult(True, map(to_dict, Url.query().fetch()))

  def addUrl(self,u):
    url = Url(status='unknown', url=u['url'])
    url.put()

    return BackendResult(True, to_dict(url))

  def updateUrl(self,u):
    url = Url.get_by_id(u['id'])
    if url is None:
      return BackendResult(False,'key not found')

    if 'status' in u:
      url.status = u['status']
    if 'url' in u:
      url.url = u['url']
      
    url.put()

    return BackendResult(True, to_dict(url))


  def deleteUrl(self,uid):
    url = Url.get_by_id(uid)
    if url is None:
      return BackendResult(False,'key not found')

    url.key.delete()

    return BackendResult(True, to_dict(url))


  def getUrl(self,uid):
    url = Url.get_by_id(uid)
    if url is None:
      return BackendResult(False,'key not found')

    return BackendResult(True, to_dict(url))

class BackendResult():

  def __init__(self, ok, result):
    if ok and type(result) is not dict and type(result) is not list:
      raise TypeError()

    self.ok = ok
    self.result = result

  def to_json(self):
    return {'ok': self.ok, 'result': self.result}
