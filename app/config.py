from dataclasses import dataclass


@dataclass(frozen=True)
class Inventory():
    dnsServers = [
        '8.26.56.26', '8.20.247.20',            # Comodo
        '1.1.1.1', '1.0.0.1',                   # Cloudflare
        '84.200.69.80', '84.200.70.40',         # DNS.WATCH
        '8.8.8.8', '8.8.4.4',                   # Google DNS
        '4.2.2.1', '4.2.2.2',                   # Level 3
        '208.67.222.222', '208.67.220.220',     # OpenDNS
        '9.9.9.9', '149.112.112.112',           # Quad9 (filtered, DNSSEC)
        '9.9.9.11', '149.112.112.11',           # Quad9 (filtered + ECS)
        '9.9.9.10', '149.112.112.10'            # Quad9 (unfiltered, no DNSSEC)
    ]
    fqdnArray = [
        "www.amazon.com",
        "www.apple.com",
        "www.aws.com",
        "www.cnn.com",
        "www.ebay.com",
        "www.espn.com",
        "www.fandom.com",
        "www.google.com",
        "wwww.facebook.com",
        "www.instagram.com",
        "www.reddit.com",
        "www.twitter.com",
        "www.windowsupdate.com",
        "www.youtube.com"
    ]


@dataclass(frozen=True)
class SystemConfigurationFiles:
    path = {
        "resolvConf": "/etc/resolv.conf",
        "systemdresolvd": "/etc/systemd/resolved.conf"
    }

    patterns = {
        "resolvconf": {
            "pattern": "nameserver [\d\.]+$\n",
            "replacement": ''
        },
        "systemdresolvd": {
            "pattern": "^#?\\bDNS\\b=?.+$\n",
            "replacement": "DNS="
        }
    }

@dataclass(frozen=True)
class UserOptions:
    options = [
        'pihole',
        'resolvconf',
        'systemdresolvd'
    ]
