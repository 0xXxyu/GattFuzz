from __future__ import absolute_import
from asyncio import wait_for

import ctypes
import errno
from platform import mac_ver
import platform
from sqlite3 import adapters
import sys
import pygatt

from bluepy import btle
from bluepy import Peripheral,UUID
from bluepy.btle import BTLEException

from future.utils import raise_

from boofuzz import exception
from boofuzz.connections import base_socket_connection, ip_constants


class BLEConnection():
   
    """
    
    Args:
        mac(str):target bt mac
        uuid(uuid)
        char_uuid(uuid)
        addr_type
        conn
    """

    def __init__(self, mac):

        self.mac = mac

    def begin(self):
        self._open()
        self._char_uuid()

    def _open(self):
        """
        connect to target BT device

        Returns:
            None
        """
        scanner = btle.Scanner(0)
        devices = scanner.scan(3.0)

        print(" Begin scan:")
        for device in devices:
            if device.addr == self.mac:
                addr_type = device.addrType
                self._conn = Peripheral(self.mac, addr_type)
                self._servies = self._conn.getServices()

    def _char_uuid(self):
        """
        print device uuid

        select write uuid

        """
        self._charWpro_uuid = {}

        for svc in self._servies:
            print("[+]        Service: ", svc.uuid)
            characteristics = svc.getCharacteristics()
            for charac in characteristics:
                uu = charac.uuid
                properties = charac.propertiesToString()
                print("    Characteristic: ", uu)
                print("        Properties: ", properties)
                if charac.supportsRead():
                    try:
                        value = charac.read()
                        print("             Value: ", value)
                    except BTLEException:
                        #print(uu+" read failed!!")
                        continue 
                if properties.find('WRITE'):
                    self._charWpro_uuid[uu]= properties
        print(60*'-')           


    '''
    def recv(self, max_bytes):
        """Receive up to max_bytes data from the target.

        Args:
            max_bytes(int): Maximum number of bytes to receive.

        Returns:
            Received data.
        """
        data = b""

        try:
            if self.bind or self.server:
                data, self._udp_client_port = self._sock.recvfrom(max_bytes)
            else:
                raise exception.SullyRuntimeError(
                    "UDPSocketConnection.recv() requires a bind address/port." " Current value: {}".format(self.bind)
                )
        except socket.timeout:
            data = b""
        except socket.error as e:
            if e.errno == errno.ECONNABORTED:
                raise_(
                    exception.BoofuzzTargetConnectionAborted(socket_errno=e.errno, socket_errmsg=e.strerror),
                    None,
                    sys.exc_info()[2],
                )
            elif e.errno in [errno.ECONNRESET, errno.ENETRESET, errno.ETIMEDOUT]:
                raise_(exception.BoofuzzTargetConnectionReset(), None, sys.exc_info()[2])
            elif e.errno == errno.EWOULDBLOCK:
                data = b""
            else:
                raise

        return data
    '''
    def write_to_char(self, data):
        """
        Send data to the target. 
        Some protocols will truncate; see self.MAX_PAYLOADS.

        Args:
            data: Data to send.

        Returns:
            int: Number of bytes actually sent.
        """
        adapter = pygatt.BGAPIBackend()


        try:
            adapter.start()
            device = adapter.connect(self.mac)

            for key in self._charWpro_uuid:                 # 先不考虑response
                device.char_write_long(key, data, wait_for_response=False)

        finally:
            adapter.stop()     
        