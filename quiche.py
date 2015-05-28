#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse


def list_gists(user, page=1):
	url = 'https://api.github.com/users/{user}/gists'.format(user=user)
	params = { 'page': page }
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
