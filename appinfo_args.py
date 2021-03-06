# MusicPlayer, https://github.com/albertz/music-player
# Copyright (c) 2013, Albert Zeyer, www.az2000.de
# All rights reserved.
# This code is under the 2-clause BSD license, see License.txt in the root directory of this project.

# Strip out MacOSX launchd -psn_... parameter.
import sys
sys.argv = [arg for arg in sys.argv if not arg.startswith("-psn_")]

try:
	import argparse
	argParser = argparse.ArgumentParser()
except ImportError:
	if len(sys.argv) > 1:
		print "Warning, argparse (for parsing sys.argv) not available. This needs Python >=2.7. Ignoring sys.argv."
	# Dummy fallback
	class DummyArgParser:
		def add_argument(self, key, **kwargs):
			if key[0:2] == "--":
				setattr(self, key[2:], False)
		def parse_known_args(self, *args, **kwargs): return self, ()
		parse_args = parse_known_args
	argParser = DummyArgParser()

argParser.add_argument(
	"--shell", action="store_true",
	help="uses a Python shell instead of the standard stdin control"
)
argParser.add_argument(
	"--pyshell", action="store_true", help="just a bare Python shell - no musicplayer stuff"
)
argParser.add_argument(
	"--pyexec", nargs=1, help="just executes the Python commands - no musicplayer stuff"
)
argParser.add_argument(
	"--qtgui", action="store_true",
	help="force Qt GUI"
)
argParser.add_argument(
	"--forkExecProc", nargs=2
)
argParser.add_argument(
	"-NSDocumentRevisionsDebugMode", nargs=1, help="MacOSX debug stuff"
)

class ArgParserExitException(Exception): pass

# Patch to avoid exit on unknown args.
def argParser_exit(status=0, message=None):
	if message:
		message = message.strip()
		print "arg parser:", message
	# Don't exit because we want to live!
	# Exceptions will be handled in appinfo.
	raise ArgParserExitException(message)
argParser.exit = argParser_exit

