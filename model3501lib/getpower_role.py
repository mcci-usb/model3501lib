##############################################################################
#
# Module: getpower_role.py
#
# Description:
#     Read the current USB Power Delivery (PD) power role
#     of the connected DUT device (Source / Sink).
#
#
# Author:
#     Vinay N, MCCI Corporation Feb 2026
#
#     V2.0.0 Mon Feb 16 2026 17:00:00   Vinay N
#         Module created
#
##############################################################################
# Built-in imports
# (None)

# Lib imports
import usb.core

# Own modules
# (None)


class getpowerRoleController:
    """
    Controller class to read DUT power role.

    This class communicates with the DUT device via
    USB control transfers to determine whether the
    device is operating as a Power Source or Sink.

    Attributes:
        vendor_id (int): USB Vendor ID of DUT device.
        product_id (int): USB Product ID of DUT device.
        device (usb.core.Device): Detected USB device instance.
    """
    def __init__(self, vendor_id, product_id):
        """
        Initialize Power Role Controller.

        Args:
            vendor_id (int): USB Vendor ID.
            product_id (int): USB Product ID.

        Returns:
            None

        Raises:
            None
        """
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
    
    def find_device(self):
        """
        Locate the USB device.

        Args:
            None

        Returns:
            bool: True if device found, False otherwise.

        Raises:
            None
        """
        self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
        return self.device is not None
    
    def get_power_role(self):
        """
        Read current DUT power role.

        Performs control transfer write/read sequence
        and compares returned data to identify whether
        DUT is operating in Source or Sink mode.

        Args:
            None

        Returns:
            None

        Raises:
            usb.core.USBError: If USB communication fails.
        """
        if self.device is None:
            print("Device not found")
            return False
        else:
            print("Device found")
        
        bmRequestType = 0x40
        bRequest = 0xE4
        wValue = 0x0000
        wIndex = 0x0000
        wLength = 0x0010
        data1 = [0x00, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        result1 = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data1)
        
        if result1 != 16:
            print("Device is None:")
            return

        bmRequestType = 0xC0
        bRequest = 0xE4
        wValue = 0x0000
        wIndex = 0x0000
        wLength = 0x0010
        result2 = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
        hex_strings = ['0x{:02X}'.format(byte) for byte in result2]
        formatted_hex_string = ' '.join(hex_strings)

        sink_data = "0x00 0x28 0x02 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00"
        source_data = "0x00 0x28 0x02 0x02 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00"

        if formatted_hex_string == sink_data:
            print("Read the current power role: SINK")
        elif formatted_hex_string == source_data:
            print("Read the current power role: SOURCE")
        else:
            print("Invalid:")

def get_power_role_status():
    """
    Entry function to read DUT power role.

    Initializes controller and triggers
    power role detection workflow.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    VENDOR_ID = 0x045e
    PRODUCT_ID = 0x078f

    controller = getpowerRoleController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.get_power_role()
