import cherrypy

import model
from firewalladmin.lib import template, http, iptables, easyadns

class DenyList:
    @cherrypy.expose
    @template.theme('denylist.html')
    def index(self):
        try:
            return template.render(message=cherrypy.session.pop('msg', None), 
                                   blacklists=model.Blacklists.select())
        except Exception, ex:
            cherrypy.session['msg'] = ex
            http.redirect('/error')
    
    @cherrypy.expose
    def rename(self, category, newname):
        bl = model.Blacklists.get(category)
        oldname = bl.category
        bl.category = newname
        iptables.rename(oldname, newname)
        cherrypy.session['msg'] = "Category %s renamed to %s." % (oldname, newname) 
        http.redirect('/denylist/');
        
    @cherrypy.expose
    def delete(self, category):
        bl = model.Blacklists.get(category)
        name = bl.category
        bl.delete(category)
        iptables.delete(name)
        cherrypy.session['msg'] = '%s category deleted.' % name
        http.redirect('/denylist/')
    
    @cherrypy.expose
    def enable(self, category):
        return self._toggle(category, True)
    
    @cherrypy.expose
    def disable(self, category):
        return self._toggle(category, False)
    
    def _toggle(self, category, enabled):
        print enabled
        try:
            bl = model.Blacklists.get(category)
            bl.enabled = enabled
            iptables.toggle(bl.category, bl.enabled)
        except Exception, ex:
            cherrypy.session['msg'] = ex
            http.redirect('/error')
        
        if enabled:
            cherrypy.session['msg'] = '%s category enabled.' % bl.category
        else:
            cherrypy.session['msg'] = '%s category disabled.' % bl.category
        http.redirect('/denylist/')
    
    @cherrypy.expose
    def new(self, category):
        model.Blacklists(category=category, blacklist='', enabled=True, ips='')
        iptables.create(category)
        cherrypy.session['msg'] = '%s category created.' % category
        http.redirect('/denylist/')
    
    @cherrypy.expose
    @template.theme('category.html')
    def category(self, category):
        try:
            return template.render(message=cherrypy.session.pop('msg', None), 
                               blacklist=model.Blacklists.get(category))
        except Exception, ex:
            cherrypy.session['msg'] = ex
            http.redirect('/error')
    
    @cherrypy.expose
    def save(self, category, blacklist=''):
        try:
            bl = model.Blacklists.get(category)
        except Exception, ex:
            cherrypy.session['msg'] = ex
            http.redirect('/error')
        
        
        cherrypy.session['msg'] = 'Blacklist updated!'
        cherrypy.session.release_lock()
        
        cleaned_bl = list()
        for line in blacklist.splitlines():
            line = line.strip()
            if line:
                cleaned_bl.append(line)
        
        """ Create blacklist """
        blacklist = "\n".join(cleaned_bl)
        
        """ Lookup IPs """
        bl.ips = "\n".join(easyadns.lookup(cleaned_bl))
                
        """ TODO: remove unresolvable domains from blacklist """
        
        """ Save blacklist """         
        bl.blacklist = blacklist
        
        """ Update firewall """
        iptables.update(bl.category, bl.ips)
        
        http.redirect('/denylist/')

