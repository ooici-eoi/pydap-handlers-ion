__author__ = 'cmueller'

import paste.script.command

def start_paster():
	from gevent import monkey; monkey.patch_all()
	from pyon.core.bootstrap import bootstrap_pyon; bootstrap_pyon()
	paste.script.command.run()