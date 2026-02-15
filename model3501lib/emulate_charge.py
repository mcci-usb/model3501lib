##############################################################################
#
# Module: emulate_charge.py
#
# Description:
#     Emulate USB Power Delivery (PD) charger profiles with
#     configurable maximum wattage levels (15W / 27W / 45W)
#     using USB control transfer commands.
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


class ChargeController:
    """
    Controller class to emulate PD charger profiles.

    This class detects the DUT device and sends USB control
    transfer commands to configure charger emulation at
    different wattage levels.

    Attributes:
        vendor_id (int): USB Vendor ID of DUT device.
        product_id (int): USB Product ID of DUT device.
        device (usb.core.Device): Detected USB device instance.
    """

    def __init__(self, vendor_id, product_id):
        """
        Initialize Charge Controller.

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
        self.device = usb.core.find(
            idVendor=self.vendor_id,
            idProduct=self.product_id
        )
        return self.device is not None

    def set_emulate_charge_15w(self, watts):
        """
        Configure DUT to emulate 15W PD charger.

        Args:
            watts (int): Requested wattage value.

        Returns:
            bool: True if command successful, False otherwise.

        Raises:
            usb.core.USBError: If USB transfer fails.
        """
        if self.device is None:
            print("Device not found")
            return False

        bmRequestType_setup = 0x40
        bRequest_setup = 0xEE
        wValue_setup = 0x0001

        data_to_send_setup = [
            0x01, 0x01, 0x2C, 0x91, 0x01, 0x04
        ]

        try:
            result_setup = self.device.ctrl_transfer(
                bmRequestType_setup,
                bRequest_setup,
                wValue_setup,
                0x0000,
                data_to_send_setup
            )

            print("Setup control transfer result for 15W:", result_setup)
            return True

        except usb.core.USBError as e:
            print(f"USBError (15W): {e}")
            return False

    def set_emulate_charge_27w(self, watts):
        """
        Configure DUT to emulate 27W PD charger.

        Args:
            watts (int): Requested wattage value.

        Returns:
            bool: True if command successful, False otherwise.

        Raises:
            usb.core.USBError: If USB transfer fails.
        """
        if self.device is None:
            print("Device not found")
            return False

        bmRequestType_setup = 0x40
        bRequest_setup = 0xEE
        wValue_setup = 0x0002

        data_to_send_setup = [
            0x01, 0x02, 0x2C, 0x91, 0x01, 0x04,
            0xB1, 0xD0, 0x02, 0x00
        ]

        try:
            result_setup = self.device.ctrl_transfer(
                bmRequestType_setup,
                bRequest_setup,
                wValue_setup,
                0x0000,
                data_to_send_setup
            )

            print("Setup control transfer result for 27W:", result_setup)
            return True

        except usb.core.USBError as e:
            print(f"USBError (27W): {e}")
            return False

    def set_emulate_charge_45w(self, watts):
        """
        Configure DUT to emulate 45W PD charger.

        Args:
            watts (int): Requested wattage value.

        Returns:
            bool: True if command successful, False otherwise.

        Raises:
            usb.core.USBError: If USB transfer fails.
        """
        if self.device is None:
            print("Device not found")
            return False

        bmRequestType_setup = 0x40
        bRequest_setup = 0xEE
        wValue_setup = 0x0003

        data_to_send_setup = [
            0x01, 0x03, 0x2C, 0x91, 0x01, 0x04,
            0x2C, 0xD1, 0x02, 0x00,
            0x2C, 0xB1, 0x04, 0x00
        ]

        try:
            result_setup = self.device.ctrl_transfer(
                bmRequestType_setup,
                bRequest_setup,
                wValue_setup,
                0x0000,
                data_to_send_setup
            )

            print("Setup control transfer result for 45W:", result_setup)
            return True

        except usb.core.USBError as e:
            print(f"USBError (45W): {e}")
            return False


def set_charge(watts):
    """
    Entry function to emulate charger wattage.

    Selects appropriate charger profile based on
    requested wattage and sends configuration
    command to DUT device.

    Args:
        watts (int): Desired charger wattage.

    Returns:
        None

    Raises:
        None
    """
    VENDOR_ID = 0x045E
    PRODUCT_ID = 0x078F

    controller = ChargeController(VENDOR_ID, PRODUCT_ID)

    if controller.find_device():

        if watts <= 15:
            controller.set_emulate_charge_15w(watts)

        elif watts <= 27:
            controller.set_emulate_charge_27w(watts)

        elif watts <= 45:
            controller.set_emulate_charge_45w(watts)

        else:
            print("Invalid wattage specified")

    else:
        print("Device not found")
