import cherrypy

def redirect(url='/'):
        raise cherrypy.HTTPRedirect(cherrypy.url(url))
        