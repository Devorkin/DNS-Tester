from config import SystemConfigurationFiles
from helpers import regex, restart_systemd_daemon


class Modifier:
    def __init__(self, user_option, filename, first_dnsServer, second_dnsServer):
        self.filename: str = filename
        self.first_dnsServer: str = first_dnsServer
        self.original_content: str = ""
        self.second_dnsServer: str = second_dnsServer
        self.user_option: str = user_option

    def apply_new_content(self, new_content: str):
        f = open(self.filename, 'w')
        f.write(new_content)
        f.close()

    def find_and_replace_pattern(self, first_dnsServer: str, second_dnsServer: str) -> str:
        if self.user_option == "resolvconf":
            self.original_content = regex(
                pattern = SystemConfigurationFiles.patterns[self.user_option]['pattern'],
                replacement = SystemConfigurationFiles.patterns[self.user_option]['replacement'],
                content = self.original_content,
            )
            self.original_content = f"{self.original_content}nameserver {self.first_dnsServer}\nnameserver {self.second_dnsServer}\n"
        
        if self.user_option == "systemdresolvd":
            updated_dns_servers_list: str = f"{first_dnsServer} {second_dnsServer}"
            regx_replacement: str = f"{SystemConfigurationFiles.patterns[self.user_option]['replacement']}{updated_dns_servers_list}\n"

            self.original_content = regex(
                pattern = SystemConfigurationFiles.patterns[self.user_option]['pattern'],
                replacement = regx_replacement,
                content = self.original_content,
            )
            self.original_content = f"{self.original_content}"
            restart_systemd_daemon(daemon_name = "systemd-resolved")
        return self.original_content

    def get_content(self):
        f = open(self.filename, 'r')
        self.original_content = f.read()
        f.close()
    
    def update_content(self):
        try:
            self.get_content()
        except:
            print("[ERR] Something BAD happened!")

        new_content:str = self.find_and_replace_pattern(first_dnsServer = self.first_dnsServer, second_dnsServer = self.second_dnsServer)
        self.apply_new_content(new_content = new_content)
