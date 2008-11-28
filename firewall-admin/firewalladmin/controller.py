import cherrypy

import model
from allowlist import AllowList
from denylist import DenyList
from firewalladmin.lib import template, http, iptables

class FirewallAdmin:
    
    """ Put List Controllers in their own files/modules/classes """
    allowlist = AllowList()
    denylist = DenyList()
    
    @cherrypy.expose
    @template.theme('index.html')
    def index(self):
        return template.render()
    
    @cherrypy.expose
    @template.theme('error.html')
    def error(self):
        return template.render(message=cherrypy.session.pop('msg', None)) 

@template.theme('login.html')
def login_page(from_page="/", username='admin', error_msg=''):
    return template.render(show_menu=False,
                           system_status='',
                           username=username,
                           message=error_msg,
                           from_page=from_page)
