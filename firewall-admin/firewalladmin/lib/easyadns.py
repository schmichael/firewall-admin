import adns, time

_dbg = False  # Enable/disable debugging messages.

easyadns_sleep = 2  # Seconds to sleep when no queries are completed 

def lookup(namelist):
    """
    Takes a list of domain names (items starting with a # will be ignored) and
    returns a set of IPs.
    """

    resolver = adns.init()
    data = set()
    results = list()  # Have to store the query objects somewhere

    for name in namelist:
        if name[0] != '#':
            results.append(resolver.submit(name, adns.rr.ADDR))

    while len(resolver.allqueries()) > 0:
        completed = resolver.completed()
        if completed:
            if _dbg: print "[easyadns] Completed: %5d" % len(completed)
            for r in completed:
                r = r.wait()
                for ip in r[3]:
                    data.add(ip[1])
        else:
            if _dbg: print "[easyadns] Sleeping..."
            time.sleep(easyadns_sleep)

    return data

