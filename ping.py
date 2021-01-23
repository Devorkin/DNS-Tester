#! /usr/bin/python3

# Needed modules
import dns.resolver
import fileinput
import time
import operator
import os
import pathlib
import platform
import re
import subprocess
import sys
from tqdm import tqdm

# Script declarations
dnsServerIndex = {}
dnsServerScores = {}
dnsServers = [ \
    '8.26.56.26', '8.20.247.20',            # Comodo \
    '1.1.1.1', '1.0.0.1',                   # Cloudflare \
    '84.200.69.80', '84.200.70.40',         # DNS.WATCH \
    '8.8.8.8', '8.8.4.4',                   # Google DNS \
    '4.2.2.1', '4.2.2.2',                   # Level 3 \
    '208.67.222.222', '208.67.220.220',     # OpenDNS \
    '9.9.9.9', '149.112.112.112',           # Quad9 (filtered, DNSSEC) \
    '9.9.9.11', '149.112.112.11',           # Quad9 (filtered + ECS) \
    '9.9.9.10', '149.112.112.10'           # Quad9 (unfiltered, no DNSSEC) \
]
fqdnArray = [ \
    "mirrorlist.centos.org", \
    "www.amazon.com", \
    "www.apple.com", \
    "www.aws.com", \
    "www.cnn.com", \
    "www.ebay.com", \
    "www.espn.com", \
    "www.fandom.com", \
    "www.google.com", \
    "wwww.facebook.com", \
    "www.instagram.com", \
    "www.pornhub.com", \
    "www.reddit.com", \
    "www.twitter.com", \
    "www.windowsupdate.com", \
    "www.youtube.com" \
]
i = 0
resolveFile='/etc/resolv.conf'

# Check CMD arguments
if len(sys.argv) == 1:
    print("This script must be run with additional parameter.")
    exit()
elif len(sys.argv) == 2:
    if sys.argv[1] == "-help":
        print("Available options:\n- PiHole\t\tEdit Pi-Hole upstream DNS servers\n- ResolvConf\t\tEdit /etc/resolv.conf")
        exit("1")
    elif sys.argv[1] == "ResolvConf":
        print("Will edit /etc/esolv.conf...")
    elif sys.argv[1] == "PiHole":
        print("Will edit Pi-Hole DNS Masq configuration...")
        print("Checking for Docker dependecies:")
        socket = pathlib.Path("/var/run/docker.sock")
        if socket.exists ():
            print ("Socket file exist")
        else:
            print ("Socket file does not exist")
        
        dockerBinary = pathlib.Path("/usr/bin/docker")
        if dockerBinary.exists ():
            print ("Docker binary exist")
        else:
            print ("Docker binary does not exist")

        libdevmapper = pathlib.Path("/usr/lib/x86_64-linux-gnu/libdevmapper.so.1.02.1")
        if dockerBinary.exists ():
            print ("Libdevmapper does exist")
        else:
            print ("Libdevmapper does not exist")

        setupVars = pathlib.Path("/usr/src/app/setupVars.conf")
        if setupVars.exists ():
            print ("setupVars file exist")
        else:
            print ("setupVars file does not exist")
    else:
        print("This argument is not supported, please use -help argument.")
        exit()
else:
    print("This script was used with too many additional parametes.")
    exit()

# Run performance tests
with tqdm(total=100, desc="Testing DNS servers performance, please wait...", bar_format="{l_bar}{bar} [ elapsed time: {elapsed} ]") as pbar:
    for server in dnsServers:
        try:
            # Run Ping tests - for latency check
            pingResponse = subprocess.check_output("ping -W 1 -{} 1 {}".format('n' if platform.system().lower() == "windows" \
                else 'c', server ), shell=True, universal_newlines=True)
            result = re.search(r'rtt min/avg/max/mdev = [\d\.]*/([\d\.]*)/[\d\.]*/[\d\.]* ms$', str(pingResponse), re.M)
            dnsServerIndex[server] = {}
            dnsServerIndex[server]['ping'] = result[1]

            # Run A record DNS resolution tests
            for fqdn in fqdnArray:
                try:
                    res = dns.resolver.Resolver(configure=False)
                    res.nameservers = [ server ]
                    t = time.process_time()
                    answers = res.resolve(fqdn, 'A')
                    elapsed_time = time.process_time() - t
                    dnsServerIndex[server][fqdn] = elapsed_time
                except dns.resolver.NXDOMAIN:
                    print(f"X\tThe DNS query \"{fqdn}\" does not exist")
                except dns.resolver.NoAnswer:
                    print(f"X\tThe DNS response for \"{fqdn}\" does not contain an answer to the question")
                except dns.resolver.NoMetaqueries:
                    print(f"X\tDNS metaqueries are not allowed")
                except dns.resolver.NoNameservers:
                    print(f"X\tAll nameservers failed to answer the query")
                except dns.resolver.NoRootSOA:
                    print(f"X\tThere is no SOA RR at the DNS root name. This should never happen!")
                    exit()
                except dns.resolver.NotAbsolute:
                    print(f"X\tAn absolute domain name is required but a relative name was provided ({fqdn})")
                except dns.resolver.YXDOMAIN:
                    print(f"X\tThe DNS query name is too long after DNAME substitution ({fqdn})")
                except dns.exception.Timeout:
                    print(f"X\tDNS operation timed out has reached ({fqdn})")
                except:
                    print(f"X\tAn unkown error occurred while querying {fqdn} using {server}")
                    continue
        except:
            continue
        # Used for TU progress bar animation
        pbar.update(int(100 / len(dnsServers)))

# Set dictionary key per DNS server
for dnsServer in dnsServerIndex:
        dnsServerScores[dnsServer] = 0

calcTemp = {}
for dnsServer in dnsServerIndex:
    calcTemp[dnsServer] = float(dnsServerIndex[dnsServer]['ping'])
calcTemp_sort = sorted(calcTemp, key=calcTemp.get)
for dnsServer_sort in calcTemp_sort:
    if i == 0:
        dnsServerScores[dnsServer_sort] = dnsServerScores[dnsServer_sort] + 1
    i = i + 1

del calcTemp
calcTemp = {}
for fqdn in fqdnArray:
    i = 0
    for dnsServer in dnsServerIndex:
        try:
            calcTemp[dnsServer] = float(dnsServerIndex[dnsServer][fqdn])
        except:
            print(f"X\t{dnsServer} failed to query {fqdn}.")
    calcTemp_sort = sorted(calcTemp, key=calcTemp.get)
    for dnsServer_sort in calcTemp_sort:
        if i == 0:
            dnsServerScores[dnsServer_sort] = dnsServerScores[dnsServer_sort] + 1
        i = i + 1

# Output the amount of ALIVE DNS servers
print(f"Amount of servers: {len(dnsServerIndex)}")
# Output the amount of DNS queries that have been used
print(f"Amount of queries: {len(dnsServerIndex[next(iter(dnsServerIndex))]) - 1}")

# Output final DNS server records, based on their performance
del calcTemp_sort
calcTemp_sort = sorted(dnsServerScores, key=dnsServerScores.get, reverse=True)

# Output all DNS servers scrores
# print("\nCurrent scrores:")
# for score in calcTemp_sort:
#     if dnsServerScores[score] != 0:
#         print(f"{score} = {dnsServerScores[score]}")

# Output the only first graded DNSD servers
i = 0
for score in calcTemp_sort:
    if i == 0:
        primaryDNS = score
        i = i + 1
    elif i == 1:
        secondaryDNS = score
        i = i + 1

if sys.argv[1] == "ResolvConf":
    # Open resolveFile for Read-Only mode
    f = open(resolveFile, 'r')
    originalContent = f.read()
    f.close()

    # Open resolveFile and append it with the winner DNS servers
    resolveNew = re.sub(r'nameserver [\d\.]+', '', originalContent)
    resolveNew = f"{resolveNew}nameserver {primaryDNS}\nnameserver {secondaryDNS}\n"

    f = open(resolveFile, 'w')
    f.write(resolveNew)
    f.close()

elif sys.argv[1] == "PiHole":
    # Edit PiHole template configuration file (setupsVars.conf)
    # Open the file in Read-Only mode
    f = open('/usr/src/app/setupVars.conf', 'r')
    originalContent = f.read()
    f.close()

    # Performing some Regex manipulation
    resolveNew = re.sub(r'PIHOLE_DNS_\d=[\d\.]+', '', originalContent).rstrip()
    resolveNew = f"{resolveNew}\nPIHOLE_DNS_1={primaryDNS}\nPIHOLE_DNS_2={secondaryDNS}\n"

    # Open the file and append it with the winner DNS servers
    f = open('/usr/src/app/setupVars.conf', 'w')
    f.write(resolveNew)
    f.close()

    # Edit PiHole running-configuration file (01-pihole.conf)
    # Open the file in Read-Only mode
    f = open('/usr/src/app/01-pihole.conf', 'r')
    originalContent = f.read()
    f.close()

    # Performing some Regex manipulation
    resolveNew = None
    resolveNew = re.sub(r'server=[\d\.]+', '', originalContent).rstrip()
    resolveNew = f"{resolveNew}\nserver={primaryDNS}\nserver={secondaryDNS}\n"

    # Open the file and append it with the winner DNS servers
    f = open('/usr/src/app/01-pihole.conf', 'w')
    f.write(resolveNew)
    f.close()

    # Restart the Pi-Hole DNS service
    subprocess.run(["docker", "exec", "-u", "0", "-it", "pihole", "bash", "-c", "pihole restartdns"])