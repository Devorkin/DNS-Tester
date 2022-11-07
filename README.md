# What is DNS-Tester?

DNS-Tester is an open-source tool that providing a way to benchmark multiple DNS servers vs. common URLs and also allows system-configuration from the tool directly.

This tool perform ping latency & resolve tests and provide scores to each test.
Based on the final score, it will recommend to use the 2 DNS servers with the best score.

This tool can also be used to configure the chosen DNS servers in your DNS system by providing its name as an argument.

Currently support the DNS systems:
* Resolv.conf
* Systemd-resolved
<br /><br />
# TODO:

* Add exceptions
* Add mechanism to automatically choose the DNS system used by the local OS (running this tool)
* Add support to run this tool via Docker-Compose or Kubernetes
* Add DNSSEC support
* Add support to the below DNS systems:
* * Bind9 (forwarders)
* * DnsMasq (upstream servers)
* * MikroTik router (via Paramiko for SSH access)
* * Pi-Hole
* * Windows OS

<br />

* Add tests
* * Network is available (publicly) for DNS & ICMP traffic
* * Write permissions to the DNS system configuration file
* * Ping tool is exists and accesiable
* * This tool process owner allowed to manage SystemD
* * etc.

* Change this tool from regular project to Python package with command-line shortcut
* Change the way that the tool handles the configuration file (using open\close twice)
* Replace the usage of `sys.agrv[]` with click or rich
* Use Ping module instead of calling it via SubProcess

<br /><br />
# Report a Bug

For filing bugs, suggesting improvements, or requesting new features, please open an [issue](https://github.com/rook/rook/issues).
<br /><br />
# Contact

Please use the following to reach members of the community:

- GitHub: Start a [discussion](https://github.com/Devorkin/DNS-Tester/discussions) or open an [issue](https://github.com/Devorkin/DNS-Tester/issues)
