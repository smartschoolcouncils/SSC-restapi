#!/usr/bin/env python3

def application(environ, start_response):
	body = b'Hello world!\n'
	start_response('200 OK', [('Content-Type', 'text/html')])
	return [body]
