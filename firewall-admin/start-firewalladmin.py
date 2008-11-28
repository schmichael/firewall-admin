#!/usr/bin/python
import cherrypy

import firewalladmin.auth
from firewalladmin.controller import FirewallAdmin

if __name__ == "__main__":
    cherrypy.quickstart(FirewallAdmin(), '/', 'firewalladmin.config')