import dns.resolver
import time
import platform
import re
import subprocess
from tqdm import tqdm


from config import Inventory
from scores import Scores


class DNS_Benchmark:
    def __init__(self):
        self.dnsServers = Inventory.dnsServers
        self.dnsServers_resolve_stats: dict = {}
        self.dnsServers_ping_latency: dict = {}
        self.first_dnsServer: str = ""
        self.fqdnArray = Inventory.fqdnArray
        self.second_dnsServer: str = ""

    def get_scores(self):
        x = Scores()
        self.first_dnsServer, self.second_dnsServer = x.score_dns_resolve_time(self.dnsServers_ping_latency, self.dnsServers_resolve_stats)
    
    @classmethod
    def ping_dns_server(cls, server: str) -> float:
        result: list = []

        try:
            pingResponse = subprocess.check_output("ping -W 1 -{} 1 {}".format('n' if platform.system().lower() == "windows" \
                else 'c', server ), shell=True, universal_newlines=True)
        except:
            return 99.0
        
        result = re.search(r'rtt min/avg/max/mdev = [\d\.]*/([\d\.]*)/[\d\.]*/[\d\.]* ms$', str(pingResponse), re.M)  # type: ignore
        return result[1]

    def run_benchmark(self):
        with tqdm(total=100, desc="Testing DNS servers performance, please wait...", bar_format="{l_bar}{bar} [ elapsed time: {elapsed} ]") as pbar:
            for dns_server in self.dnsServers:
                ping_latency = float(self.ping_dns_server(dns_server))
                if ping_latency == 99.0:
                    continue
                self.dnsServers_resolve_stats[dns_server] = {}
                self.dnsServers_ping_latency[dns_server] = ping_latency    
                # Run A record DNS resolution tests
                for fqdn in self.fqdnArray:
                    res = dns.resolver.Resolver(configure=False)
                    res.nameservers = [dns_server]
                    current_time = time.process_time()
                    try:
                        res.resolve(fqdn, 'A')
                    except:
                        self.dnsServers_resolve_stats[dns_server][fqdn] = float(99)
                        continue
                    elapsed_time = time.process_time() - current_time
                    self.dnsServers_resolve_stats[dns_server][fqdn] = float(f"{elapsed_time:.5f}")
                # Used for TU progress bar animation
                pbar.update(int(100 / len(self.dnsServers)))
        self.get_scores()
