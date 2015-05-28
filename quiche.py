#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse

GISTS_PER_PAGE = 100


def list_gists(user, page=1):
	"""
	Returns a list of gists for a given user.
	"""
	url = 'https://api.github.com/users/{user}/gists'.format(user=user)
	params = { 'page': page, 'per_page': GISTS_PER_PAGE }
	return request('get', url, params=params)


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
		return json.loads(res)
