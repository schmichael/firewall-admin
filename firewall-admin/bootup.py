#!/usr/bin/python
from firewalladmin import model
from firewalladmin.lib import iptables, bridge

#bridge.startup()
iptables.startup()

for category in model.Blacklists.select():
	iptables.create(category.category)
	iptables.update(category.category, category.ips)
	if not category.enabled:
		iptables.toggle(category.category, category.enabled)
