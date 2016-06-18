"""
Factory for the implementation of a listener on a unicast address of a local network interface
"""
import logging
import netifaces
import socket
from ipaddress import IPv6Address

from dhcpkit.common.server.config_elements import ConfigElementFactory
from dhcpkit.ipv6 import SERVER_PORT
from dhcpkit.ipv6.server.listeners import Listener
from dhcpkit.ipv6.utils import is_global_unicast

logger = logging.getLogger()


class UnicastListenerFactory(ConfigElementFactory):
    """
    Factory for the implementation of a listener on a unicast address of a local network interface
    """

    def validate_config(self):
        """
        Validate the interface information
        """
        try:
            socket.if_nametoindex(self.interface)
        except OSError:
            raise ValueError("Interface {} not found".format(self.interface))

        interface_addresses = [IPv6Address(addr_info['addr'].split('%')[0])
                               for addr_info
                               in netifaces.ifaddresses(self.interface).get(netifaces.AF_INET6, [])]

        # Validate what the user supplied
        unicast_address = IPv6Address(self._section.getSectionName())
        if not is_global_unicast(unicast_address):
            raise ValueError("The listener address must be a global unicast address")

        if unicast_address not in interface_addresses:
            raise ValueError("Cannot find unicast address {} on interface {}".format(self._section.reply_from,
                                                                                     self.interface))

    def create(self) -> Listener:
        """
        Create a listener of this class based on the configuration in the config section.

        :return: A listener object
        """
        address = IPv6Address(self._section.getSectionName())
        interface_name = self._section.interface
        interface_addresses = [IPv6Address(addr_info['addr'].split('%')[0])
                               for addr_info
                               in netifaces.ifaddresses(interface_name).get(netifaces.AF_INET6, [])]

        if address not in interface_addresses:
            raise ValueError("Cannot find address {} on interface {}".format(address, interface_name))

        logger.debug("Creating socket for {} on {}".format(address, self._section.interface))

        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((str(address), SERVER_PORT))
        return Listener(self._section.interface, sock)