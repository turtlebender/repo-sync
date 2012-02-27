#!/bin/bash

chmod +x /var/lib/repo-sync/bin/*
ln -s /var/lib/repo-sync/bin/repopull /usr/local/bin/
ln -s /var/lib/repo-sync/bin/repopush /usr/local/bin/
ln -s /var/lib/repo-sync/bin/reposync /usr/local/bin/
