#! /usr/bin/python3

import sys


from benchmark import DNS_Benchmark
from config import SystemConfigurationFiles, UserOptions
from helpers import print_results
from modifier import Modifier


def __main__():
    if len(sys.argv) == 1:
        print_help_msg()
    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == "-help" or sys.argv[1].lower() == "-h" :
            print_help_msg()
            exit()
        
        if sys.argv[1].lower() == "manual" or sys.argv[1].lower() in UserOptions.options:
            x = DNS_Benchmark()
            x.run_benchmark()
            if sys.argv[1].lower() == "manual":
                print("Benchmark scores:")
                print(print_results(first_dnsServer = x.first_dnsServer, second_dnsServer = x.second_dnsServer))
            else:
                modifier = Modifier(filename = SystemConfigurationFiles.path[sys.argv[1].lower()], 
                                first_dnsServer = x.first_dnsServer,
                                second_dnsServer = x.second_dnsServer,
                                user_option = sys.argv[1].lower()
                            )
                modifier.update_content()
                print(print_results(first_dnsServer = x.first_dnsServer, second_dnsServer = x.second_dnsServer))
        else:
            print_help_msg()
    else:
        print_help_msg()

def print_help_msg():
    print("====================================================================================================================")
    print("This script must be run with additional parameter.")
    print("Available options:\n \
        - Manual\t\tRun DNS banchmark tests without performing any system change\n \
        - PiHole\t\tEdit Pi-Hole upstream DNS servers\n \
        - ResolvConf\t\tEdit /etc/resolv.conf\n \
        - SystemdResolvD\tEdit /etc/systemd/resolved.conf")
    print("====================================================================================================================\n")

if __name__ == "__main__":
    __main__()
