import os

def startup():
    _cmd("iptables -F")
    _cmd("iptables -t nat -F")
    _cmd("iptables -t nat -N CATEGORIES")
    _cmd("iptables -t nat -N BLOCKED_ACTIONS")
    _cmd("iptables -t nat -A PREROUTING -p TCP --dport 80 -j CATEGORIES")
    _cmd("iptables -t nat -A PREROUTING -p TCP --dport 443 -j CATEGORIES")
    _cmd("iptables -t nat -A BLOCKED_ACTIONS -p TCP --dport 80 -j DNAT --to-destination 192.168.100.123:8888")
    _cmd("iptables -t nat -A BLOCKED_ACTIONS -p TCP --dport 443 -j DROP")
#    _cmd("iptables -t nat -I CATEGORIES -p tcp -m state --state ESTABLISHED -j RETURN")

def create(name):
    _cmd("iptables -t nat -N cat_%s" % name)
    _cmd("iptables -t nat -A CATEGORIES -j cat_%s" % name) 

def delete(name):
    _cmd("iptables -t nat -D CATEGORIES -j cat_%s" % name) 
    _cmd("iptables -t nat -X cat_%s" % name)

def rename(old_name, new_name):
    _cmd("iptables -t nat -E cat_%s cat_%s" % (old_name, new_name))

def toggle(name, enable):
    if enable:
        _cmd("iptables -t nat -A CATEGORIES -j cat_%s" % name)    
    else:
        _cmd("iptables -t nat -D CATEGORIES -j cat_%s" % name)
    
def update(name, blacklist):
    _cmd("iptables -t nat -F cat_%s" % name)
    for line in blacklist.splitlines():
        _cmd("iptables -t nat -A cat_%s -d %s -j BLOCKED_ACTIONS" % (name, line)) 



def whitelist_add(ip, site):
    _cmd("iptables -t nat -I CATEGORIES -s %s -d %s -j RETURN" % (ip, site))
    
def whitelist_remove(ip, site):
    _cmd("iptables -t nat -D CATEGORIES -s %s -d %s -j RETURN" % (ip, site))

iptables_debug = False 

def _cmd(cmd):
    if iptables_debug:
        print cmd
    os.system(cmd)
