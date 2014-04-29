#!/usr/bin/env python
import commands
import ntpath

import alfred

results = []

def addResult(title, subtitle, icon):
  global results
  results.append(alfred.Item(
      attributes= {'uid': alfred.uid(0), 'arg': ''},
      title=title,
      subtitle=subtitle,
      icon=icon
  ))

def getDigest(filename, alg):
  digest = commands.getstatusoutput('openssl dgst -'+ alg +' ' + filename)
  return digest[1].split('= ')[1]

def checkDigest(filename, digest, alg):
  c_digest = getDigest(filename, alg)
  if digest == c_digest:
    addResult(alg.upper() + ' MATCH for \''+ ntpath.basename(filename) + '\'',  '[' + c_digest + ']', 'icons/green.png')
    return True
  return False

(filename, digest) = alfred.args()

if not checkDigest(filename, digest, 'sha1'):
  if not checkDigest(filename, digest, 'md5'):
    if not checkDigest(filename, digest, 'sha256'):
      addResult('NO MATCH for \''+ ntpath.basename(filename) + '\'', 'file may be corrupted!', 'icons/red.png')

alfred.write(alfred.xml(results))
