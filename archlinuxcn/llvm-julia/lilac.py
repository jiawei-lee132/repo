#!/usr/bin/env python3

from lilaclib import *
from pyalpm import vercmp

prefix = 'refs/tags/julia-'

def _get_new_version(major):
  ver_prefix = f'{prefix}{major}.'
  tags = s.get("https://api.github.com/repos/JuliaLang/llvm-project/git/refs/tags").json()
  max_ver = ''
  for tag in tags:
    if not tag.get('ref', '').startswith(ver_prefix):
      continue
    ver = tag['ref'].removeprefix(prefix)
    if not max_ver or vercmp(ver, max_ver):
      max_ver = ver
  return max_ver

def pre_build():
  if _G.newver != _G.newvers[1]:
    raise ValueError('Upstream LLVM version mismatch, manual update required.')
  julia_ver_commit = _G.newvers[3]
  julia_ver = _get_new_version(_G.newver)
  if julia_ver_commit:
    if julia_ver:
      raise ValueError('New tagged release available.')
    pkgver, julia_commit = julia_ver_commit.split('-', 2)
    for line in edit_file('PKGBUILD'):
      if line.startswith('_julia_rel='):
        line = f'_julia_rel='
      if line.startswith('_julia_commit='):
        line = f'_julia_commit={julia_commit}'
      print(line)
  else:
    if not julia_ver:
      raise ValueError('Cannot find new version')
    pkgver, julia_rel = julia_ver.split('-', 2)
    for line in edit_file('PKGBUILD'):
      if line.startswith('_julia_rel='):
        line = f'_julia_rel={julia_rel}'
      if line.startswith('_julia_commit='):
        line = f'_julia_commit='
      print(line)
  update_pkgver_and_pkgrel(pkgver)
