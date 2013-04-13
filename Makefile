# This Makefile constructs a web interface for cc.py, using cc_eval.py and the
# webinclude directory. It uses a slightly patched version of pyjs 0.8.1a
# (https://github.com/pyjs/pyjs/pull/792).
#
# Be sure to change the pyjsbuildroot variable below to point to your pyjs
# installation.

# Variables
target = cc_eval
outputdir = weboutput
pyjsbuildroot = $(HOME)/installs/pyjs.git

pyjsbuild = $(pyjsbuildroot)/bin/pyjsbuild

# Flags
targetfile = $(target).nocache.html
pyjsopts = -I webinclude -o $(outputdir) --no-compile-inplace

# Use this for developing
# pyjsopts += -c --strict
# pyjsopts += -d

# Use this for the public interface
pyjsopts += -c -O

pyjs: $(outputdir)/$(targetfile)

$(outputdir)/$(targetfile): webinclude/* webinclude/public/* Makefile *.py webinclude/examples.py
	echo Making web version using pyjsbuild.
	test -f $(pyjsbuild)
	test -d $(outputdir) || mkdir -p $(outputdir)
	$(pyjsbuild) $(pyjsopts) $(target)

webinclude/examples.py: build-examples.py webinclude/examples/*.cc webinclude/examples
	python3 build-examples.py > webinclude/examples.py

continuous-pyjs: pyjs
	$(pyjsbuild) $(pyjsopts) --auto-build $(target)


clean:
	rm -Rf $(outputdir) __pycache__ *.pyc
	rm -f buffer.js cc.js webinclude/cc_eval.js webinclude/io.js
	# rm -Rf *.????????????????????????????????.js webinclude/*.????????????????????????????????.js

.PHONY: clean pyjs continuous-pyjs