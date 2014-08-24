# FRIMM Makefile

# set DESTDIR variable if not
ifndef $(DESTDIR)
  DESTDIR=/
endif

PYTHRUN=python2

all:
	$(PYTHRUN) setup.py build

install:
	$(PYTHRUN) setup.py install --root=$(DESTDIR)

clean:
	$(PYTHRUN) setup.py clean
	rm -f MANIFEST
	rm -rf build dist
	find . -name '*.pyc' -exec rm {} \;

export camelCAPS='[a-z_][a-zA-Z0-9_]*$$'
export StudlyCaps='[a-zA-Z_][a-zA-Z0-9_]*$$'

check:
	pylint --indent-string="    " --class-rgx=${StudlyCaps} --function-rgx=${camelCAPS} --method-rgx=${camelCAPS} --variable-rgx=${camelCAPS} --argument-rgx=${camelCaps} waktu/waktu waktu/*.py

tarball:
	$(PYTHRUN) setup.py sdist

rpm: tarball
	rpmbuild -tb dist/frimm-*.tar.gz
	mv ~/rpmbuild/RPMS/noarch/* dist/

run:
	cd scripts ; $(PYTHRUN) frimm ; cd ..
