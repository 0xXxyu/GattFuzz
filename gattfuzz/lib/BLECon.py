import asyncio
import platform
import sys

from bleak import BleakScanner
from bleak import BleakClient
from gattfuzz.lib.Logger import Logger

logger = Logger(loggername='Main').get_logger()

class BLECon():

    def __init__(self, mac) -> None:
        self._mac = mac
        self.handles = []
        self._client = None

    def notification_handler(self, sender, data):
        """Simple notification handler which prints the data received."""
        print("{0}: {1}".format(sender, data))

    async def print_char(self):

        device = await BleakScanner.find_device_by_address(self._mac, timeout=10.0)
        if device == None:
            print("未扫描到目标设备，请查看设备状态重试。")
            sys.exit(0)
        logger.info(f"Find target device: {device}")
        
        async with BleakClient(self._mac) as self._client:
            for service in self._client.services:
                print("-"*60)
                logger.info(f"++[Service] {service}")
                for char in service.characteristics:
                    logger.info(f"\t[Characteristic] {char}")
                    logger.info(f"\t\t char.properties: {char.properties}")
                    if "read" in char.properties:
                        try:
                            value = bytes(await self._client.read_gatt_char(char.uuid))
                            logger.info(
                                f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                            )
                        except Exception as e:
                            logger.error(
                                f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}"
                            )

                    elif "write-without-response" in char.properties:
                        # print("no response writechar\n")
                        # print(char.handle)
                        if char.handle not in self.handles:
                            self.handles.append(char.handle)
                        # pass

                    elif "write" in char.properties:
                        # print("write char\n")
                        # print(char.handle)
                        if char.handle not in self.handles:
                            self.handles.append(char.handle)
                        # pass

                    elif "notify" in char.properties:
                        # TODO
                        await self._client.start_notify(char.handle, self.notification_handler)
                        # print("notify char\n")
                        # pass
                        
                    else:
                        value = None
                        logger.info(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                        )

                    for descriptor in char.descriptors:
                        try:
                            value = bytes(
                                await self._client.read_gatt_descriptor(descriptor.handle)
                            )
                            logger.info(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                        except Exception as e:
                            logger.error(f"\t\t[Descriptor] {descriptor}) | Value: {e}")
            await self._client.disconnect()

    async def write_to_handle(self, hand, val):

        import binascii
        if type(val) != bytes:
            val = binascii.a2b_hex(val)
        if self._client.is_connected:
            await self._client.write_gatt_char(hand, val)
            logger.info(f'write value: {val} to handle: {hand}')
            await asyncio.sleep(5.0)
        else:
            try:
                async with BleakClient(self._mac) as self._client:
                    await self._client.write_gatt_char(hand, val)
                    logger.info(f'write value: {val} to handle: {hand}')
                    await asyncio.sleep(3.0)    
            except Exception as e:
                logger.error("设备断开，请查看写入数据并尝试重试。")
                logger.exception(e)


    
    async def write_val(self, dic):
        for key in dic.keys():
            for v in dic[key]:
                await self.write_to_handle(key, v)


# m = "8c:ce:fd:5d:ca:5d"
# ble = BLECon(m)
# # ble.tar_con()
# # ble.print_char()
# logging.basicConfig(level=logging.INFO)
# asyncio.run(ble.print_char())
# # print(ble.handles)
# asyncio.run(ble.write_to_handle(15, 'AAAA0112'))