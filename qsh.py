#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
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
	description="Runs a script from a user's gists.",
)

arg_parser.add_argument(
	'script', help='A path to a script in the form `user/filename`.',
)

arg_parser.add_argument(
	'arguments', help='Arguments passed to the script as-is.',
	             metavar='arguments...',
	             nargs=argparse.REMAINDER,
)


def fetch_user_script(username, filename):
	"""
	Searches for a gist containing the given file name.
	"""
	gists = fetch_user_gists(username)
	gistfile = find_file_in_gists(gists, filename)
	return request('get', gistfile['raw_url']).get('text')


def fetch_user_gists(username, page=1):
	"""
	Returns a list of gists for a given user.
	"""
	url = 'https://api.github.com/users/{user}/gists'.format(user=username)
	params = { 'page': page, 'per_page': GISTS_PER_PAGE }
	return request('get', url, params=params).get('json')


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


def request(method, url, params=None, data=None, headers=None):
	"""
	Make a request to an URL, with optional query parameters
	or body data.
	"""
	if params is not None:
		params = urllib.parse.urlencode(params)
		url = '{}?{}'.format(url, params)
	if data is not None:
		kwargs['data'] = json.dumps(data)
	if headers is None:
		headers = {}
	headers['Content-Type'] = 'application/json;charset=utf-8'
	request = urllib.request.Request(
		url     = url,
		headers = headers,
		method  = method.upper(),
		data    = data,
	)
	with urllib.request.urlopen(request) as response:
		text_content = response.read().decode('utf-8')
		try:
			json_content = json.loads(text_content)
		except ValueError:
			json_content = None
		return {
			'status': response.status,
			'reason': response.reason,
			'headers': response.getheaders(),
			'text': text_content,
			'json': json_content,
		}
			

if __name__ == '__main__':
	args = arg_parser.parse_args()
	script = parse_user_script_path(args.script)
	contents = fetch_user_script(script['username'], script['filename'])
	arguments = args.arguments or []
	# Store the contents to a named temporary file and make it
	# executable so that it is callable with subprocess.
	with tempfile.NamedTemporaryFile(delete=True) as f:
		f.write(contents.encode('utf-8')) and f.flush()
		os.chmod(f.name, stat.S_IRUSR|stat.S_IXUSR)
		subprocess.call([ f.name ] + arguments, stdin=sys.stdin)
