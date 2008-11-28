import cherrypy

import model
from firewalladmin.lib import template, http, iptables

class AllowList:
    @cherrypy.expose
    @template.theme('allowlist.html')
    def index(self):	
    	return template.render(allowlist=model.AllowList.select(),
							   message=cherrypy.session.pop('msg', None))
    
    @cherrypy.expose
    def delete(self, id):
    	al = model.AllowList.get(id)
    	rule = al.internal
        for line in al.allowlist.splitlines():
        	iptables.whitelist_remove(rule, line)
        al.delete(id)
        cherrypy.session['msg'] = 'Deleted allow list for internal IP %s' % rule
        http.redirect('/allowlist/')
    
    @cherrypy.expose
    def new(self, internal, allow_list):
    	cleaned_lines = list()
    	for line in allow_list.splitlines():
    		line = line.strip()
    		if line:
    			cleaned_lines.append(line)
    			iptables.whitelist_add(internal, line) # Update firewall
    	allow_list = "\n".join(cleaned_lines)
    	
    	al = model.AllowList(internal=internal, allowlist=allow_list)
    	cherrypy.session['msg'] = 'Created allow list for internal IP %s' % internal
    	http.redirect('/allowlist/')
    	
