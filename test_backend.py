import unittest
from backend import Backend, BackendResult
from models import Url
from google.appengine.ext import testbed

class TestBackend(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.backend = Backend()
    cls.testbed = testbed.Testbed()
    cls.testbed.activate()
    cls.testbed.init_datastore_v3_stub()
    cls.testbed.init_memcache_stub()

  @classmethod
  def tearDownClass(cls):
    cls.testbed.deactivate()

  def test_get(self):
    res = self.backend.getUrls()
    self.assertTrue(res.ok)

  def test_add(self):
    res = self.backend.addUrl({'url':'http://aaaa'})
    self.assertTrue(res.ok)
    self.assertTrue(res.result['status'] == 'unknown')

  def test_update(self):
    res = self.backend.addUrl({'url':'http://bbbb'})
    self.assertTrue(res.ok)

    res = self.backend.getUrl(res.result['id'])
    self.assertTrue(res.ok)

    res = self.backend.updateUrl({'id': res.result['id'], 'status': 'ok'})
    self.assertTrue(res.ok)

    res = self.backend.getUrl(res.result['id'])
    self.assertTrue(res.ok)
    self.assertTrue(res.result['status'] == 'ok')

  def test_delete(self):
    res = self.backend.addUrl({'url':'http://bbbb'})
    self.assertTrue(res.ok)

    res = self.backend.getUrl(res.result['id'])
    self.assertTrue(res.ok)

    newRes = self.backend.deleteUrl(res.result['id'])
    self.assertTrue(res.ok)

    res = self.backend.getUrl(res.result['id'])
    self.assertFalse(res.ok)
    

if __name__ == '__main__':
  unittest.main()