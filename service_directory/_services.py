#!/usr/bin/env python

'''
services.py
A module that reads the database of services running on the node and those found via avahi (mdns) and spits them out for use elsewhere.
'''

__author__ = 'Haxwithaxe (me at haxwithaxe dot net)'

from _utils import *

# grab shared config
conf = config()

def get_local_services_list():
	'''
	Get the list of services running on this node from the databases.
	'''
	import sqlite3
	# Define the location of the service database.
	servicedb = conf.servicedb
	service_list = []

	# Set up a connection to the database.
	debug("DEBUG: Opening service database.",5)
	connection = sqlite3.connect(servicedb)
	cursor = connection.cursor()

	# Pull a list of running web apps on the node.
	debug("DEBUG: Getting list of running webapps from database.",5)
	cursor.execute("SELECT name FROM webapps WHERE status='active';")
	results = cursor.fetchall()
	for service in results:
		service_list += [{'name':service[0],'path':service[0]}]

	# Pull a list of daemons running on the node. This means that most of the web apps users will access will be displayed.
	debug("DEBUG: Getting list of running servers from database.",5)
	cursor.execute("SELECT name,showtouser FROM daemons WHERE status='active';")
	results = cursor.fetchall()
	for service in results:
		debug("DEBUG: Value of service: %s" % service)
		# Test to see if the daemon is one that can be shown to the user.  If it's not, skip to the next iteration.
		if service[1] == 'no': debug("DEBUG: This daemon won't be shown to the user.")
		service_list += [{'name':service[0],'path':service[0],'description':''}]

		# Clean up after ourselves.
		debug("DEBUG: Closing service database.",5)
		cursor.close()
	return service_list

def get_remote_services_list():
	'''
	Get list of services advertised by Byzantium nodes found by avahi.
	'''
	import re
	service_list = []
	srvcdict = file2json(conf.services_cache)
	for name, vals in srvcdict.items():
		if re.find('__byz__._tcp',name):
			description = ''
			path = vals['host']
			if vals['port']: path += str(vals['port'])
			if vals['text'] not in ('','\x00'):
				for entry in vals['text'].split('\n'):
					key,val = (entry+'=').split('=')
					v = list(val)
					v.pop(-1)
					val = ''.join(v)
					if key == conf.uri_post_port_string_key:
						path += val
					elif key == conf.service_description_key:
						description += val
			name = re.sub('__byz__\._[udtcp]{3}.*','',name)
			service_list = [{'name':name,'path':path,'description':desciption}]
	return service_list

def get_services_list():
	return get_local_services_list()+get_remote_services_list()

if __name__ == '__main__':
	debug(get_services_list(),0)
