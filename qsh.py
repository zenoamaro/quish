#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import json
import stat
import argparse
import tempfile
import subprocess
import urllib.request
import urllib.parse

GISTS_PER_PAGE = 100

match_user_script_path = re.compile(r"""
	(?P<username>[\w\d]+)
	/
	(?P<filename>[^/]+)
""", re.VERBOSE)


arg_parser = argparse.ArgumentParser(
	description="Runs a script from a user's gists."
)

arg_parser.add_argument(
	'script', help='A path to a script in the form `user/filename`.'
)


def fetch_user_script(username, filename):
	"""
	Searches for a gist containing the given file name.
	"""
	gists = fetch_user_gists(username)
	gistfile = find_file_in_gists(gists, filename)
	return request('get', gistfile['raw_url'])


def fetch_user_gists(username, page=1):
	"""
	Returns a list of gists for a given user.
	"""
	url = 'https://api.github.com/users/{user}/gists'.format(user=username)
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


def parse_user_script_path(path):
	"""
	Parses a script path into its components.

	>>> parse_user_script_path('user/script-name.sh') \
	    == { 'filename':'script-name.sh', 'username':'user' }
	True
	"""
	match = match_user_script_path.match(path)
	if not match: raise ValueError('Invalid script path, `{}`.'.format(path))
	return match.groupdict()


def filename_matches(a, b):
	"""
	Tries to matches two filenames exactly, then by basename.

	>>> filename_matches('file', 'file.sh')
	True
	"""
	return (a == b) \
	    or (basename(a) == basename(b))


def basename(filename):
	"""
	Returns a filename without the extension.

	>>> basename('file.sh')
	'file'

	>>> basename('.file')
	'.file'
	"""
	return filename.rsplit('.', 1)[0]\
	    or filename


def request(method, url, params=None, data=None):
	if params:
		params = urllib.parse.urlencode(params)
		url = '{}?{}'.format(url, params)
	req = urllib.request.Request(
		url,
		method = method.upper(),
	)
	with urllib.request.urlopen(req) as f:
		res = f.read()
		try:
			return json.loads(res.decode('utf-8'))
		except ValueError:
			return res
			

if __name__ == '__main__':
	args = arg_parser.parse_args()
	script = parse_user_script_path(args.script)
	contents = fetch_user_script(script['username'], script['filename'])
	# Store the contents to a named temporary file and make it
	# executable so that it is callable with subprocess.
	with tempfile.NamedTemporaryFile(delete=True) as f:
		f.write(contents) and f.flush()
		os.chmod(f.name, stat.S_IRUSR|stat.S_IXUSR)
		subprocess.call([ f.name ])
