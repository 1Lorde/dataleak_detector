from api import offline_check
from config import logger
from utils import get_mac, get_user, get_local_ip, block_linux, block_win


def create_extra(event_type, device_properties):
    extra = {}
    if event_type == 'LINUX_USB_ADD':
        extra = {
            'dev_action': device_properties.get('ACTION'),
            'dev_serial': device_properties.get('ID_SERIAL_SHORT'),
            'dev_type': device_properties.get('DEVTYPE'),
            'dev_model': device_properties.get('ID_MODEL'),
            'dev_model_from_db': device_properties.get('ID_MODEL_FROM_DATABASE'),
            'dev_name': device_properties.get('DEVNAME'),
            "dev_valid": offline_check(device_properties.get('ID_SERIAL_SHORT'))
        }
    elif event_type == 'LINUX_USB_REMOVE':
        extra = {
            'dev_action': device_properties.get('ACTION'),
            'dev_name': device_properties.get('DEVNAME'),
        }
    elif event_type == 'WIN_USB_ADD':
        extra = {
            'dev_action': 'add',
            'dev_model': device_properties.get('vendor_id') + device_properties.get('product_id'),
            'dev_serial': device_properties.get('serial_number'),
            "dev_valid": offline_check(device_properties.get('serial_number'))
        }

    extra["host_mac"] = get_mac()
    extra["host_ip"] = get_local_ip()
    extra["host_user"] = get_user()

    return extra


def watch_drives_linux():
    import pyudev

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    for device in iter(monitor.poll, None):
        if device.action == 'add' and device.properties.get('BUSNUM'):
            props = device.properties
            extra = create_extra("LINUX_USB_ADD", props)
            if extra["dev_valid"]:
                logger.info(
                    f'Registered USB-device detected [User:{extra["host_user"]}, IP:{extra["host_ip"]}, MAC:{extra["host_mac"]},' 
                    f' Serial: {extra["dev_serial"]}, Model(DB):{extra["dev_model_from_db"]}, Model:{extra["dev_model"]}]',
                    extra=extra)
            else:
                logger.info(
                    f'INVALID USB-DEVICE DETECTED [User:{extra["host_user"]}, IP:{extra["host_ip"]}, MAC:{extra["host_mac"]},'
                    f' Serial: {extra["dev_serial"]}, Model(DB):{extra["dev_model_from_db"]}, Model:{extra["dev_model"]}]',
                    extra=extra)
            print('[USB-device watch] ' + str(extra))
            block_linux(extra["host_user"])
        elif device.action == 'remove' and device.properties.get('BUSNUM'):
            props = device.properties
            extra = create_extra("LINUX_USB_REMOVE", props)
            logger.info(
                f'USB-device removed [User:{extra["host_user"]}, IP:{extra["host_ip"]}, MAC:{extra["host_mac"]}].',
                extra=extra)
            print('[USB-device watch] ' + str(extra))


def watch_drives_win():
    import pythoncom
    pythoncom.CoInitialize()
    import wmi as wmi
    # raw_wql = "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_USBHub'"
    c = wmi.WMI()
    watcher = c.watch_for(notification_type='Creation', wmi_class='Win32_USBHub', delay_secs=2)

    while True:
        usb = watcher()
        id_property = usb.wmi_property("DeviceId").value
        device_properties = {
            "vendor_id": id_property.split("\\")[1].split("&")[0],
            "product_id": id_property.split("\\")[1].split("&")[1],
            "serial_number": id_property.split("\\")[2],
        }

        extra = create_extra("WIN_USB_ADD", device_properties)
        if extra["dev_valid"]:
            logger.info(
                f'Registered USB-device detected: User:{extra["host_user"]}, IP:{extra["host_ip"]}, MAC:{extra["host_mac"]},'
                f' Serial: {extra["dev_serial"]}.',
                extra=extra)
        else:
            logger.info(
                f'INVALID USB-device detected: User:{extra["host_user"]}, IP:{extra["host_ip"]}, MAC:{extra["host_mac"]},'
                f' Serial: {extra["dev_serial"]}.',
                extra=extra)
            block_win(extra["host_user"])
        print('[USB-device watch]' + str(extra))
