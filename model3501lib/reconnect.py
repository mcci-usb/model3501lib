##############################################################################
#
# Module: reconnect.py
#
# Description:
#     Disconnect and reconnect the Type-C MUTT device once,
#     with optional delay timings (in milliseconds) before
#     disconnect and before reconnect operations.
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
import usb.util

# Own modules
# (None)

class ReconnectController:
    """
    Controller class to perform MUTT reconnect operation.

    This class detects the Type-C MUTT device and sends a
    vendor-specific USB control transfer command to trigger
    disconnect and reconnect events with configurable delays.

    Attributes:
        vendor_id (int): USB Vendor ID of DUT device.
        product_id (int): USB Product ID of DUT device.
        device (usb.core.Device): Detected USB device instance.
    """
    def __init__(self, vendor_id, product_id):
        """
        Initialize Reconnect Controller.

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

    def disconnect_and_reconnect(self, delay_disconnect_ms, delay_reconnect_ms):
        """
        Perform disconnect and reconnect sequence.

        Sends a USB control transfer command to trigger
        MUTT disconnect followed by reconnect after
        specified delay intervals.

        Args:
            delay_disconnect_ms (int):
                Delay before disconnect (milliseconds).

            delay_reconnect_ms (int):
                Delay before reconnect (milliseconds).

        Returns:
            bool: True if command executed successfully,
                  False otherwise.

        Raises:
            usb.core.USBError:
                If USB communication fails.
        """
        if self.device is None:
            print("Device not found")
            return False
        
        # Set configuration
        self.device.set_configuration()
        
        # Setup packet details
        bmRequestType = 0x40  # Request type: Vendor, Host-to-device, Device-to-interface
        bRequest = 0x10       # Request code
        wLength = 0x00

        # Send control transfer for disconnect
        self.device.ctrl_transfer(bmRequestType, bRequest, delay_disconnect_ms, delay_reconnect_ms, wLength)
        print(f"Device disconnected for {delay_disconnect_ms}ms and reconnected for {delay_reconnect_ms}ms")
        return True

def reconnect_status(delay_disconnect_ms, delay_reconnect_ms):
    """
    Entry function to trigger reconnect operation.

    Initializes controller and executes disconnect/
    reconnect workflow with provided delay timings.

    Args:
        delay_disconnect_ms (int):
            Delay before disconnect (milliseconds).

        delay_reconnect_ms (int):
            Delay before reconnect (milliseconds).

    Returns:
        None

    Raises:
        None
    """
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = ReconnectController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.disconnect_and_reconnect(delay_disconnect_ms, delay_reconnect_ms)
