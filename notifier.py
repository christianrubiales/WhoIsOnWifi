import csv, os, tailer

for line in tailer.follow(open('whoisonwifi.log')):
	csv_reader = csv.reader([line])
	components = None
	for row in csv_reader:
		components = row
	components.pop(0)
	body = "\n".join(components)
	os.system('ntfy -t "Who Is On Wifi?" send "\n'+body+'"')
