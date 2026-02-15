##############################################################################
#
# Module: cdstress_on.py
#
# Description:
#     Enable Connect-Disconnect (CD) Stress operation on the DUT device
#     using USB control transfer commands.
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


class CDstressONController:
    """
    Controller class to enable Connect-Disconnect (CD) Stress.

    This class locates the USB DUT device using Vendor ID and
    Product ID, and sends a control transfer command to enable
    CD stress operation.

    Attributes:
        vendor_id (int): USB Vendor ID of the DUT device.
        product_id (int): USB Product ID of the DUT device.
        device (usb.core.Device): Detected USB device instance.
    """

    def __init__(self, vendor_id, product_id):
        """
        Initialize CD Stress ON controller.

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
        Locate the USB device using Vendor ID and Product ID.

        Args:
            None

        Returns:
            bool: True if device is found, False otherwise.

        Raises:
            None
        """
        self.device = usb.core.find(
            idVendor=self.vendor_id,
            idProduct=self.product_id
        )
        return self.device is not None

    def set_cdstress_on(self):
        """
        Send control transfer command to enable CD Stress.

        Args:
            None

        Returns:
            bool: True if command executed successfully, False otherwise.

        Raises:
            usb.core.USBError: If USB communication fails.
        """
        if self.device is None:
            print("Device not found")
            return False

        # USB Control Transfer parameters
        bmRequestType = 0x40
        bRequest = 0xE8
        wValue = 0x0000
        wIndex = 0x0001
        wLength = 0x0000

        # Send control transfer
        result = self.device.ctrl_transfer(
            bmRequestType,
            bRequest,
            wValue,
            wIndex,
            wLength
        )

        print("result_cd_stress:", result)

        return result == 0

    def setup_cd_stress_on(self):
        """
        Complete workflow to enable CD Stress.

        This function finds the device and sends the
        CD Stress ON command.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        if self.find_device():
            if self.set_cdstress_on():
                print("CD Stress ON command sent successfully")
            else:
                print("Failed to send CD Stress ON command")
        else:
            print("Device not found")


def onset_cdstress():
    """
    Entry function to enable CD Stress.

    This function initializes the controller with
    predefined Vendor ID and Product ID and triggers
    the CD Stress ON workflow.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    VENDOR_ID = 0x045E
    PRODUCT_ID = 0x078F

    controller = CDstressONController(VENDOR_ID, PRODUCT_ID)
    controller.setup_cd_stress_on()
