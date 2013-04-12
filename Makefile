# Variables
target = cc_eval
outputdir = weboutput
# pyjsbuildroot = $(HOME)/installs/pyjamas-0.7
pyjsbuildroot = $(HOME)/installs/pyjs.git

pyjsbuild = $(pyjsbuildroot)/bin/pyjsbuild

# Flags
targetfile = $(target).nocache.html
pyjsopts = -I webinclude -o $(outputdir) --no-compile-inplace
pyjsopts += -c --strict
# pyjsopts += -d
# pyjsopts += -c -O

pyjs: $(outputdir)/$(targetfile)

$(outputdir)/$(targetfile): webinclude/* webinclude/public/* Makefile *.py
	echo Making web version using pyjsbuild.
	test -f $(pyjsbuild)
	test -d $(outputdir) || mkdir -p $(outputdir)
	$(pyjsbuild) $(pyjsopts) $(target)

continuous-pyjs: pyjs
	$(pyjsbuild) $(pyjsopts) --auto-build $(target)


clean:
	rm -Rf $(outputdir) __pycache__ *.pyc
	rm -f buffer.js cc.js webinclude/cc_eval.js webinclude/io.js
	# rm -Rf *.????????????????????????????????.js webinclude/*.????????????????????????????????.js

.PHONY: clean pyjs continuous-pyjs