##############################################################################
#
# Module: getrdo.py
#
# Description:
#     Read the (RDO) corresponding to the
#     current USB Power Delivery power contract between the
#     system and the Type-C MUTT device.
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

class getrdoController:
    """
    Controller class to read current PD RDO.

    This class communicates with the DUT device using USB
    control transfers to retrieve the active Request Data
    Object (RDO) representing the negotiated power contract.

    Attributes:
        vendor_id (int): USB Vendor ID of DUT device.
        product_id (int): USB Product ID of DUT device.
        device (usb.core.Device): Detected USB device instance.
    """
    def __init__(self, vendor_id, product_id):
        """
        Initialize RDO Controller.

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
    
    def get_rdo(self):
        """
        Read the current RDO

        Performs a two-stage USB control transfer:
        1. Send request command.
        2. Read back RDO response data.

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
        data1 = [0x00, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        result1 = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data1)
        print("result-1:", result1)
        
        if result1 == 16:
            bmRequestType = 0xC0
            bRequest = 0xE4
            wValue = 0x0000
            wIndex = 0x0000
            wLength = 0x0010
            result2 = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
            hex_strings = ['0x{:02X}'.format(byte) for byte in result2]
            formatted_hex_string = ' '.join(hex_strings)
            print("Read the RDO for the current power contract:", formatted_hex_string)
        else:
            print("No RDO: no power contract in place between the system and the Type-C MUTT")

def get_rdo_status():
    """
    Entry function to read RDO status.

    Initializes controller and retrieves
    active power contract RDO data.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    VENDOR_ID = 0x045e
    PRODUCT_ID = 0x078f

    controller = getrdoController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.get_rdo()
