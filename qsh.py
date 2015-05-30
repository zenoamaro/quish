#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse

GISTS_PER_PAGE = 100


def fetch_user_script(user, filename):
	"""
	Searches for a gist containing the given file name.
	"""
	gists = fetch_user_gists(user)
	gistfile = find_file_in_gists(gists, filename)
	if gistfile: return request('get', gistfile['raw_url'])


def fetch_user_gists(user, page=1):
	"""
	Returns a list of gists for a given user.
	"""
	url = 'https://api.github.com/users/{user}/gists'.format(user=user)
	params = { 'page': page, 'per_page': GISTS_PER_PAGE }
	return request('get', url, params=params)


def find_file_in_gists(gists, target):
	"""
	Searches for a particular file by name in a list of gists.
	"""
	for gist in gists:
		for filename, contents in gist['files'].items():
			if filename_matches(filename, target):
				return contents


def basename(filename):
	"""
	Returns a filename without the extension.
	"""
	return filename.rsplit('.', 1)[0]


def filename_matches(a, b):
	"""
	Tries to matches two filenames exactly, then by basename.
	"""
	return a == b \
	    or basename(a) == basename(b)


def request(method, url, params=None, data=None):
	if params:
		params = urllib.parse.urlencode(params)
		url = '{}?{}'.format(url, params)
	req = urllib.request.Request(
		url,
		method = method.upper(),
	)
	with urllib.request.urlopen(req) as f:
		res = f.read().decode('utf-8')
		try:
			return json.loads(res)
		except ValueError:
			return res
			
