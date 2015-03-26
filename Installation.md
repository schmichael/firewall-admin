# Introduction #

A basic knowledge of working with Linux on the command line is required, and a basic knowledge of iptables and Python would probably help.

The firewall allows creating multiple blacklists (aka Categories) which can be edited/paused/deleted individually. It has has allow lists (aka Whitelists) which can be used to allow specific internal IPs access to specific sites that might otherwise be blocked by a blacklist.

This little setup has proved very useful at a public school district for augmenting their existing content filtering system, and all web traffic passes through it without trouble. An old PIII can run a 3,000 domain blacklist at 10mbps while using less than 10% of the CPU.

# Directions #

  1. Copy the firewall-admin code to your "new" dedicated firewall computer. By default its setup to be in `/srv/firewall-admin`
  1. If you didn’t extract to `/srv/firewall-admin`, edit `etc/rc.local` and `basedir` in `firewalladmin.config` to reflect the your directory.
  1. By default `firewalladmin/lib/bridge.py` bridges `eth1` and `eth2`, and `eth0` should be attached to your LAN to access SSH and the web control panel.
  1. Edit `firewalladmin.config` to run on the IP address assigned to your administrative NIC and remember what port its set to run on.
  1. Add the commands from `etc/rc.local` to your system’s existing `/etc/rc.local` script. This will start the transparent firewall and web control panel on boot.
  1. Next you’ll need to setup the database. Edit line 28 in `firewalladmin/model.py` to set a default password and then run `createdb.py`
  1. You're now ready to start the firewall and control panel simply by running `sudo etc/rc.local`. You can always test out just the web interface by running `start-firewalladmin.py`
  1. Browse to the web interface using the IP and Port setup in step 4, login using the username and password setup in step 6, and start configuring your transparent firewall!

## Setup the blocked page ##

When a user visits a blocked site they are redirected to the IP and Port specified on line 10 of `firewalladmin/lib/iptables.py`. We setup Apache to listen on that port and serve up a generic You’ve been blocked page, but you could be even more clever. You’ll need a `.htaccess` file like the following to properly map all blocked traffic to your block page:

```
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.html [L,QSA]
```

# Caveats #

  * All scripts as well as the web control panel are executed as root. This setup should only be run on dedicated hardware and not on a server with other services.
  * No test suite. Mea culpa.
  * Little to no error handling. You’ve been warned. ;)
  * Basically this is a quick hack and should not be used in the same way you use tested and maintained software. YMMV