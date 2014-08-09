#!/usr/bin/env python
import commands
import ntpath

import alfred

results = []
algs = ['sha1', 'md5', 'sha256']

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

def checkDigests(filename, digest):
  global algs
  match = False
  for alg in algs:
    c_digest = getDigest(filename, alg)
    if digest == c_digest:
      match = True
      addResult(alg.upper() + ' MATCH for \''+ ntpath.basename(filename) + '\'',  '[' + c_digest + ']', 'icons/green.png')
  if not match:
    addResult('NO MATCH for \''+ ntpath.basename(filename) + '\'', 'file may be corrupted!', 'icons/red.png')

def showAllDigests(filename):
  global algs
  for alg in algs:
    c_digest = getDigest(filename, alg)
    addResult(alg.upper() + ' for \''+ ntpath.basename(filename) + '\'',  ' is [' + c_digest + ']', 'icons/orange.png')

# main
(filename, digest) = alfred.args()

if digest == 'all':
  showAllDigests(filename)
else:
  checkDigests(filename, digest)

alfred.write(alfred.xml(results))
