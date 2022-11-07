import re
import subprocess

def print_results(first_dnsServer: str, second_dnsServer: str):
    return f"The best servers to use are: {first_dnsServer}, {second_dnsServer}"

def regex(pattern: str, replacement: str, content: str, count: int = 0):
    new_content = re.sub(
        r"{}".format(pattern),
        "{}".format(replacement),
        content,
        count = count,
        flags = re.MULTILINE
    )
    return new_content

def restart_systemd_daemon(daemon_name: str):
    try:
        subprocess.check_output("systemctl daemon-reload", shell=True, universal_newlines=True)
    except:
        print(f"[ERR]Failed to relad SystemD daemons configurations")
        exit(1)

    try:
        subprocess.check_output(f"systemctl restart {daemon_name}", shell=True, universal_newlines=True)
    except:
        print(f"[ERR]Failed to restart SystemD daemon {daemon_name}")
        exit(1)
    