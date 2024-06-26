# model3501lib

MCCI Model 3501 SuperMUTT Python based library for control and operation

<!--
  This TOC uses the VS Code markdown TOC extension AlanWalk.markdown-toc.
  We strongly recommend updating using VS Code, the markdown-toc extension and the
  bierner.markdown-preview-github-styles extension. Note that if you are using
  VS Code 1.29 and Markdown TOC 1.5.6, https://github.com/AlanWalk/markdown-toc/issues/65# cricketlib

This is a Python library to s the MCCI USB Switches (switch 3201,2301, 3141, 3142, 2101) and supports to Cricket UI.

<!--
  This TOC uses the VS Code markdown TOC extension AlanWalk.markdown-toc.
  We strongly recommend updating using VS Code, the markdown-toc extension and the
  bierner.markdown-preview-github-styles extension. Note that if you are using
  VS Code 1.29 and Markdown TOC 1.5.6, https://github.com/AlanWalk/markdown-toc/issues/65
  applies -- you must change your line-ending to some non-auto value in Settings>
  Text Editor>Files.  `\n` works for me.
-->
<!-- markdownlint-disable MD033 MD004 -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->
<!-- TOC depthFrom:2 updateOnSave:true -->

- [Install python](#install-python37-32-bit-package)
- [Prerequisites for running or building](#prerequisites-for-running-or-building)
- [Requiremets](#requirements)
- [package usage](#package-usage)
- [Installing package via pip cmd](#installing-package-via-pip-cmd)
- [Development](#development)
- [Demo](#demo)

- [Release History](#release-history)


### Install Python3.7 (32-bit) package 
install python package from [python.org](https://www.python.org/ftp/python/3.7.8/python-3.7.8.exe)


### Install Python3.7 (64-bit) package
install python package from [python.org](https://www.python.org/ftp/python/3.7.8/python-3.7.8-amd64.exe)

### Install pip package
```shell
pip --version
python -m pip install --upgrade pip
```

### Prerequisites for running or building

<strong>On Windows:</strong>

Development environment
* OS - Windows 10 and 11 64 bit
* Python - 3.7.8
* pyusb - 1.2.1

```shell
pip install pyusb

```


### Installing model3501lib Packages

1.  Clone the repository from [github](https://github.com/mcci-usb/model3501lib.git)

2.  Open a `cmd terminal` and change directory to  `{path_to_repository}/model3501lib`. using `cd` into the root directory where setup.py is located

3.  To install the library in your local Python setup, enter the command in Windows OS
```bash
python setup.py sdist bdist_wheel

python install .
```

Please navigate to dist/ directory and you will find the files .egg file.
Example: `model3501api-1.0.0-py3.7.egg`

## package usage
Create a Python file named `Simpletest.py` and open in text editor and import the `model3501lib` modules.

```python
#import the time for using delay between each commnds
import time
```
### Sending a cmd for find device details
```python
# To show list of the Model3501 devices.
# import FindDeviceController
from model3501lib import FindDeviceController, find_device_status

# Command
find_device_status()
```
### Sending a cmd for Set Speed
```python
#Set to speed: s is super speed , h is high speed, l is low speed
# import DeviceController
from model3501lib import DeviceController, set_speed

# Command
set_speed('s')
set_speed('h')
set_speed('l')
```
### Sending a cmd for Emulate Charge
```python
#Emulate a PD charger with max watts 'W'.
 #15W (5V 3.0A)
 #27W (9V 3.0A)
 #45W (15V 3.0A)
 #set_charge(w)

 # import ChargeController
 from model3501lib import ChargeController, set_charge

 # Command
 set_charge(15) #15 is Example
```
### Sending a cmd for CDStressOn
```python
#Enable connect disconnect stress
# import CDstressONController
from model3501lib import CDstressONController, onset_cdstress

# Command
onset_cdstress()
```

### Sending a cmd for CDStressOff
```python
# Disable connect disconnect stress

# import CDstressOFFController
from model3501lib import CDstressOFFController, offset_cdstress

# Command
offset_cdstress()
```

### Sending a cmd for Reconnect X Y
```python
# Disconnect and reconnect the Type-C MUTT one time with
#optional wait times (in ms), X before disconnect,and Y beforereconnect.
# Test reconnect functionality with specified delays

# import ReconnectController
from model3501lib import ReconnectController, reconnect_status

# Command
delay_disconnect_ms = 5000  # 1 second
delay_reconnect_ms = 10000  # 1 second
reconnect_status(delay_disconnect_ms, delay_reconnect_ms)
```

### Sending a cmd for PdChargerPort
```python
# Switch PD to charger receptacle.

# import PDChargerPortController
from model3501lib import PDChargerPortController, pd_charger_port_status

# Command
pd_charger_port_status()
```

### Sending a cmd for PdCaptiveCable
```python
#  Switch PD to captive cable

# import PDCaptiveCablesController
from model3501lib import PDCaptiveCablesController

# Command
pd_captive_cables_status()
```
### Sending a cmd for GetRdo
```python
#  Read the RDO for the current power contract.

# import getrdoController
from model3501lib import getrdoController, get_rdo_status

# Command
get_rdo_status()
```
### Sending a cmd for GetPowerRole
```python
#  Read the current power role.

# import getpowerRoleController
from model3501lib import getpowerRoleController, get_power_role_status

# Command
get_power_role_status()
```
## Installing package via pip cmd
```python
pip install model3501api
```

## Development
- It is a fully independent package.
All necessary things are installed during the normal installation process.
- currently works and tested only for Windows.

## Demo

![Demo Video](assets/mcci-model.gif)

## Release History
- Initial release
