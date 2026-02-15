##############################################################################
#
# Module: findDevice.py
#
# Description:
#     Detect and list connected Type-C MUTT devices by
#     Vendor ID and Product ID. Retrieves device details
#     such as manufacturer, product name, firmware version,
#     and USB speed.
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
import usb.util

# Own modules
# (None)

class FindDeviceController:
    """
    Controller class to detect MUTT USB devices.

    This class scans all connected USB devices and filters
    them based on Vendor ID and Product ID. It retrieves
    device descriptor information and USB speed details.

    Attributes:
        vendor_id (int): Target USB Vendor ID.
        product_id (int): Target USB Product ID.
        device (usb.core.Device): USB device instance.
    """
    def __init__(self, vendor_id, product_id):
        """
        Initialize Find Device Controller.

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
        Scan and list matching USB devices.

        This function searches all connected USB devices,
        filters by VID/PID, retrieves descriptor details,
        and determines USB speed.

        Args:
            None

        Returns:
            list: List of dictionaries containing device details.

        Raises:
            usb.core.USBError: If descriptor retrieval fails.
        """
        devices_info = []

        # Find all USB devices connected to the system
        devices = usb.core.find(find_all=True)
        
        # Iterate through each device and check if it matches the target VID and PID
        for device in devices:
            # Check if the device has both VID and PID attributes
            if device.idVendor is not None and device.idProduct is not None:
                # Check if the device matches the target VID and PID
                if device.idVendor == self.vendor_id and device.idProduct == self.product_id:
                    # Perform control transfer to retrieve device descriptor
                    try:
                        bmRequestType = 0x40  # Direction: IN
                        bRequest = 0x14        # GET_DESCRIPTOR request
                        wValue = 0x0000
                        wIndex = 0x0000
                        wLength = 0x0000
                        
                        result = device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
                        if result == 0:
                            speed = "High speed"
                        else:
                            speed = "Super speed"
                        
                        # Retrieve device information
                        manufacturer = usb.util.get_string(device, device.iManufacturer)
                        product = usb.util.get_string(device, device.iProduct)
                        firmware_version = device.bcdDevice

                        # Create a dictionary with device information including USB speed
                        device_info = {
                            'vendor_id': hex(self.vendor_id),
                            'product_id': hex(self.product_id),
                            'manufacturer': manufacturer,
                            'product': product,
                            'firmware_version': firmware_version,
                            'speed': speed
                        }
                        devices_info.append(device_info)
                    except usb.core.USBError as e:
                        print(f"Failed to retrieve device descriptor: {e}")
        
        return devices_info

def find_device_status():
    """
    Entry function to list MUTT device status.

    Detects all matching devices and prints their
    descriptor and speed information.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    VENDOR_ID = 0x045e
    PRODUCT_ID = 0x078f
    controller = FindDeviceController(VENDOR_ID, PRODUCT_ID)
    devices = controller.find_device()

    # Print the device information directly
    if devices:
        for device in devices:
            print(f"Vendor ID: {device['vendor_id']}, Product ID: {device['product_id']}, Manufacturer: {device['manufacturer']}, Product: {device['product']}, Firmware Version: {device['firmware_version']}, Speed: {device['speed']}")
    else:
        print("No matching devices found.")

# Example usage
find_device_status()
