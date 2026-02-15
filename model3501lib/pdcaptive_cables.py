##############################################################################
#
# Module: pdcaptive_cables.py
#
# Description:
#     Switch USB Power Delivery (PD) operation to Captive Cable
#     mode on the connected Type-C MUTT device using vendor-
#     specific USB control transfer commands.
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

class PDCaptiveCablesController:
    """
    Controller class to switch PD mode to Captive Cable.

    This class detects the MUTT device and sends a USB
    vendor-specific control transfer command to enable
    captive cable PD operation.

    Attributes:
        vendor_id (int): USB Vendor ID of DUT device.
        product_id (int): USB Product ID of DUT device.
        device (usb.core.Device): Detected USB device instance.
    """
    def __init__(self, vendor_id, product_id):
        """
        Initialize PD Captive Cable Controller.

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
    
    def pd_captive_cables(self):
        """
        Switch PD operation to Captive Cable mode.

        Sends vendor-specific control transfer command
        to configure captive cable support.

        Args:
            None

        Returns:
            bool: True if command successful, False otherwise.

        Raises:
            usb.core.USBError: If USB communication fails.
        """
        if self.device is None:
            print("Device not found")
            return False
        
        # Control transfer parameters for PdCaptiveCable
        bmRequestType = 0x40  # Request type: Vendor, Host-to-device, Device-to-interface
        bRequest = 0xE9       # Request code for PdCaptiveCable command
        wValue = 0x0000       # Value
        wIndex = 0x0000       # Index
        wLength = 0x0000      # Length

        # Send control transfer for PdCaptiveCable command
        result = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
        print("result-pd-captive-cables:", result)
        if result == 0:
            print("Switched PD support to captive cable successfully")
        else:
            print("Failed to switch PD support to captive cable")
        return result == 0

def pd_captive_cables_status():
    """
    Entry function to enable Captive Cable PD mode.

    Initializes controller and triggers captive
    cable configuration workflow.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = PDCaptiveCablesController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.pd_captive_cables()
