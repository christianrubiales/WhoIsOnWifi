import datetime, json, nmap, time

print('\nWho Is On WiFi?')
print('https://github.com/christianrubiales/WhoIsOnWifi')
print('Use Ctrl+C to exit\n')

# read config
with open('config.json') as f:
	data = json.load(f)
	interval_seconds = data["interval_seconds"]
	hosts_argument = data["hosts"]

# populate knowns lookup
knowns = {}
for known in data["knowns"]:
	knowns[known["mac"].lower()] = known["name"]

hosts = {}

def get_mac_from_nmap(host, nm):
	mac = ''
	if 'mac' in nm[host]['addresses']:
		mac = nm[host]['addresses']['mac'].lower()
	return mac

def log(nm, host, action, mac, vendor):
	msg = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
	msg = '","'.join([msg, action, mac, host])

	if mac not in knowns:
		msg = '","'.join([msg, 'UNKNOWN'])
	else:
		msg = '","'.join([msg, knowns[mac]])
	msg = '","'.join([msg, vendor])
	msg = '"%s"' % (msg)
	print(msg)
	with open('whoisonwifi.log','a') as f:
		f.write(msg+'\n')

nm = nmap.PortScanner()
while True:
	data = nm.scan(hosts_argument, arguments='-sn')

	# check who left
	all_hosts = nm.all_hosts()
	for host in set(hosts.keys()).difference(all_hosts):
		log(nm, host, 'LEFT', hosts[host], '')
		hosts.pop(host)

	# check connected hosts
	for host in all_hosts:
		if host not in hosts.keys():
			mac = get_mac_from_nmap(host, nm)
			hosts[host] = mac

			vendor = ''
			if len(nm[host]['vendor']) > 0:
				key = next(iter(nm[host]['vendor']))
				vendor = nm[host]['vendor'][key]

			log(nm, host, 'JOIN', mac, vendor)
	time.sleep(interval_seconds)
