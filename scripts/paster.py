__author__ = 'cmueller'

import paste.script.command

def start_paster():
	from gevent import monkey; monkey.patch_all()
	paste.script.command.run()