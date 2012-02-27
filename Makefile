VIRTUAL_ENV_DIR=dist
INSTALL_DIR=/var/lib/repo-sync
GEMS_PREFIX=/var/lib/gems/1.8
.PHONY: build

build:
	virtualenv --no-site-packages $(VIRTUAL_ENV_DIR)
	$(VIRTUAL_ENV_DIR)/bin/python setup.py install
	virtualenv --relocatable $(VIRTUAL_ENV_DIR)

install: build
	test -d $(INSTALL_DIR) || $(INSTALL_DIR) 
	cp -r $(VIRTUAL_ENV_DIR)/* $(INSTALL_DIR)
	chmod +x $(INSTALL_DIR)/bin/repo*
	test -e /usr/local/bin/repopull || ln -s $(INSTALL_DIR)/bin/repopull /usr/local/bin/repopull
	test -e /usr/local/bin/repopush || ln -s $(INSTALL_DIR)/bin/repopush /usr/local/bin/repopush
	test -e /usr/local/bin/reposync || ln -s $(INSTALL_DIR)/bin/reposync /usr/local/bin/reposync

clean:
	rm -rf $(VIRTUAL_ENV_DIR)
	find ./ -name "*.pyc" -delete

deb: build
	PATH=${PATH}:$(GEMS_PREFIX)/bin fpm -h >/dev/null || (echo "You must install fpm: gem install fpm --no-ri --no-rdoc" ; exit 1;)
	test -d debian/build/var/lib/repo-sync || mkdir -p debian/build/var/lib/repo-sync
	cp -r $(VIRTUAL_ENV_DIR)/* debian/build/var/lib/repo-sync
	fpm -s dir -t deb -C debian/build/ -d "inotify-tools (>= 3.13)" -n python-reposync -v 0.1 --post-install debian/post-install.sh --pre-uninstall debian/pre-uninstall.sh

