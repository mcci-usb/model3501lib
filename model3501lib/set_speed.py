
##############################################################################
#
# Module: set_speed.py
#
# Description:
#     Configure the USB operating speed of the connected
#     Type-C MUTT device. Supported speed modes include:
#
#         s → SuperSpeed
#         h → High Speed
#         f → Full Speed
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

class DeviceController:
    """
    Controller class to configure MUTT USB speed.

    This class detects the MUTT device and sends
    vendor-specific USB control transfer commands
    to switch the USB link operating speed.

    Attributes:
        vendor_id (int): USB Vendor ID of DUT device.
        product_id (int): USB Product ID of DUT device.
        device (usb.core.Device): Detected USB device instance.
    """
    def __init__(self, vendor_id, product_id):
        """
        Initialize Device Speed Controller.

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
    
    def set_device_speed(self, speed_type):
        """
        Set MUTT USB operating speed.

        Args:
            speed_type (str):
                Desired speed mode:
                    's' → SuperSpeed
                    'h' → High Speed
                    'f' → Full Speed

        Returns:
            bool: True if command successful, False otherwise.

        Raises:
            usb.core.USBError:
                If USB communication fails.
        """
        if self.device is None:
            print("Device not found")
            return False
        
        bmRequestType = 0x40
        if speed_type == 's':
            bRequest = 0x15  # Super Speed request
        elif speed_type == 'h':
            bRequest = 0x14  # High Speed request
        elif speed_type == 'f':
            bRequest = 0x13  # Full Speed request
        else:
            print("Invalid speed type")
            return False
        
        wValue = 0x0000
        wIndex = 0x0000
        wLength = 0x0000

        result = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)

        if result == 0:
            print(f"Set {speed_type} speed successfully\n")
        else:
            print("Device is not found:\n")

def set_speed(speed_type):
    """
    Entry function to configure device speed.

    Initializes controller and applies requested
    USB speed configuration.

    Args:
        speed_type (str):
            Desired speed mode:
                's' → SuperSpeed
                'h' → High Speed
                'f' → Full Speed

    Returns:
        None

    Raises:
        None
    """
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = DeviceController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.set_device_speed(speed_type)
