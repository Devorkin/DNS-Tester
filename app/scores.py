from json import dumps


from config import Inventory


class Scores:
    def __init__(self):
        self.dnsServers: list = Inventory.dnsServers
        self.fqdnArray: list = Inventory.fqdnArray

    @classmethod
    def score_ping_latency(cls, dnsServers_ping_latency: dict) -> tuple:
        dnsServers_per_ping_latency = sorted(dnsServers_ping_latency, key=dnsServers_ping_latency.get)    # type: ignore
        return dnsServers_per_ping_latency[0], dnsServers_per_ping_latency[1]

    def score_dns_resolve_time(self, dnsServers_ping_latency: dict, dnsServers_resolve_stats: dict) -> tuple:
        first_dnsServer, second_dnsServer = self.score_ping_latency(dnsServers_ping_latency)

        calcScore = {}
        for dnsServer in self.dnsServers:
            calcScore[dnsServer] = 0

        for fqdn in self.fqdnArray:
            calcTemp: dict = {}
            for dnsServer in self.dnsServers:
                try:
                    calcTemp[dnsServer] = dnsServers_resolve_stats[dnsServer][fqdn]
                except:
                    print("[ERR] Details will be presented below:")
                    print(f"\t[ERR] {dnsServer} -- {fqdn}")
                    print(f"{dumps(dnsServers_resolve_stats[dnsServer], indent=2)}")
            calcScore[sorted(calcTemp, key=calcTemp.get)[0]]+=1  # type: ignore
            del calcTemp

        calcScore[first_dnsServer]+=len(self.fqdnArray)
        calcScore[second_dnsServer]+=len(self.fqdnArray)/2
        calcScore2 = sorted(calcScore, key=calcScore.get, reverse=True)  # type: ignore
        return calcScore2[0], calcScore2[1]
