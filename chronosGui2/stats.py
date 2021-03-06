# -*- coding: future_fstrings -*-

from urllib.request import urlopen
import json
import logging; log = logging.getLogger('Chronos.perf')

import chronosGui2.api as api

report_url = 'http://192.168.1.55:19861'
contact_warned = False
def report(tag: str, data: dict):
	"""Report program statistics to an internal server, stats.node.js."""
	assert tag
	assert "tag" not in data
	assert "serial_number" not in data
		
	data["tag"] = tag
	data["serial_number"] = api.control().getSync('cameraSerial')
	try:
		urlopen(report_url, bytes(json.dumps(data), 'utf-8'), 0.1)
	except Exception:
		global contact_warned
		if not contact_warned:
			contact_warned = True
			log.warn(f'Could not contact the stats server at {report_url}.')
		pass
	
def report_mock(tag: str, data: dict):
	"""Report program statistics to nothing."""
	pass