# minimalistic server example from 
# https://github.com/seprich/py-bson-rpc/blob/master/README.md#quickstart
import json
import re
import socket
from bsonrpc import JSONRpc
from bsonrpc import request, service_class
from bsonrpc.exceptions import FramingError
from bsonrpc.framing import (
	JSONFramingNetstring, JSONFramingNone, JSONFramingRFC7464)


# Class providing functions for the client to use:
@service_class
class ServerServices(object):

  @request
  def increment(self, txt):
    dictionary = {}
    txt = txt.strip()
    # split on whitespace and punctuation
    #words = re.split('[^A-Za-z1-9]', txt)
    childrens = {}
    nodes = json.loads(txt)
    #https://pythonspot.com/json-encoding-and-decoding-with-python/
    for x in nodes['children']:
      if x['name'] in childrens:
        childrens[x['name']] += 1

      else:
        childrens[x['name']] = 1
    for x in nodes['children']:
      if x['name'] in childrens:
        x['val'] += childrens[x['name']]

    nodes['val'] += 1
    #from pprint import pprint
    #pprint(dump(nodes))

    rootJSON = json.dumps(nodes, default=lambda inc: inc.__dict__)
    return rootJSON#''.join(r)


#https://stackoverflow.com/questions/383944/what-is-a-python-equivalent-of-phps-var-dump@Zoredache
def dump(obj):
  '''return a printable representation of an object for debugging'''
  newobj=obj
  if '__dict__' in dir(obj):
    newobj=obj.__dict__
    if ' object at ' in str(obj) and not newobj.has_key('__type__'):
      newobj['__type__']=str(obj)
    for attr in newobj:
      newobj[attr]=dump(newobj[attr])
  return newobj

# Quick-and-dirty TCP Server:
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 50001))
ss.listen(10)

while True:
  s, _ = ss.accept()
  # JSONRpc object spawns internal thread to serve the connection.
  JSONRpc(s, ServerServices(),framing_cls=JSONFramingNone)
