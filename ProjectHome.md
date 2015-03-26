Web content filter that uses `iptables` to block both `http` and `https` requests.

**Note** that this project is not being actively developed, so use at your own risk.  It has been successfully used in a school district with hundreds of computers.  It worked beautifully there, but your mileage may vary.

_Anyone interested in actively maintaining this project please don't hesitate to contact the project administrators._

# Features #

  * Simple to install: put your dedicated firewall computer between your router and LAN.
  * Nice [CherryPy](http://www.cherrypy.org) web based control panel for ease of use.
  * Categories
  * White-list (internal ip to external site)

# Requirements #

  * Old computer to use as dedicated firewall.
    * Pentium III is fast enough to handle at least 10mbps throughput with 3,000 domains in the blocklist.
    * 3 NICs: 1 incoming, 1 outgoing, 1 for the administrative interface.
  * Linux - only tested on [Debian Etch](http://www.debian.org/releases/etch/).
  * Required software:
    * `iptables` - tested with 1.3.6
    * `bridge-utils` - for `brctl`; tested with 1.2
    * Python - tested with 2.4
    * [CherryPy](http://www.cherrypy.org/wiki/CherryPyDownload) - at least 3.0.1
    * [Genshi](http://genshi.edgewall.org/wiki/Download) - tested with 0.4
    * `python-adns` - tested with 1.1.0
    * SQLObject - tested with 0.7.1
    * SQLite & python-sqlite
    * python-formencode

# Installation #

See [Installation](Installation.md) wiki page.

## Credits ##

  * Kyle Waremburg for the idea, writing the `iptables` code, and creating the Google Code project.
  * [Michael Schurter](http://michael.susens-schurter.com/) for the web interface
