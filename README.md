# SpaceMouse Omniverse Kit Extension

This repository contains an Isaac Sim extension with:
* A device driver class supporting the full range of SpaceMouse devices. 
* UI for tuning sensitivity and plotting output signal
* USD-based forwarder which will make device input available to other extensions via USD properties

Tested with Isaac Sim 2022.2.1 and 2023.1.1.

This extension can be used standalone as a spacemouse driver on Isaac Sim for your own applications.
See [Fast Explicit-Input Assistance for Teleoperation in Clutter](https://github.com/NVlabs/fast-explicit-teleop) for an example of using the spacemouse device for robot teleoperation.

## Installation

Clone into `~/Documents/Kit/apps/Isaac-Sim/exts`, and rename the folder `srl.spacemouse`

The code depends on the `hid` Python module to read input from a SpaceMouse. To install it into the Isaac Sim Python environment, use the Python shim in the Isaac Sim installation folder:

    ./python.sh -m pip install hidapi

### SpaceMouse Installation (Ubuntu)

Install device drivers from your distribution:

    sudo apt install spacenavd

With your device plugged in, you should now be able to run `lsusb` and see an entry with `3Dconnexion Space Navigator` in the name. The two hex numbers after "ID" are the vendor and product IDs.

Create a udev rule in `/etc/udev/rules.d/99-spacemouse.rules` to correctly configure the permissions for the device (using the IDs you just acquired with `lsusb`):

    SUBSYSTEM=="usb", ATTRS{idVendor}=="256f", ATTRS{idProduct}=="c652", MODE="0666", SYMLINK+="spacemouse"

Unplug and plug back in the device and you should see `/dev/spacemouse` appear in the filesystem, indicating that the rules took effect.

## Usage

You must include this ext as a dependency in your `extension.toml`:
    ```
    [dependencies]
    "srl.spacemouse" = {}
    ```

Then you have two choices of how to use the device in your extension.

### Via Extension

The extension will manage the lifecycle of a driver object and will present basic UI for connecting to and configuring the device. Using the device this way is simpler at the expense of some flexibility.

1. Open `SRL > SpaceMouse`, select the device you have and click `Engage`.
2. In your source code, to access the controls:

    ```python
    from srl.spacemouse.spacemouse_extension import get_global_spacemouse
    spacemouse = get_global_spacemouse()
    stamp, trans, rot, raw_buttons = spacemouse.get_controller_state()
    ```

### Via Python

Instantiate the `SpaceMouse` class correctly and read the control signal. You are responsible for ensuring that the object is destroyed correctly when your extension shuts down, or you may lose the ability to connect to the device until you relaunch.


## Development

Run `source ${ISAAC_SIM_ROOT}/setup_python_env.sh` in a shell, then run `code .` in the repository. The included `.vscode` config is based on the one distributed with Isaac Sim.

Omniverse will monitor the Python source files making up the extension and automatically "hot reload" the extension when you save changes.


## Contributions

An initial version of the code was based on a sample from Ajay Mandlekar. Later versions make extensive use of the [pyspacenavigator](https://github.com/johnhw/pyspacenavigator) project (MIT license).

If you find this codebase useful, please star or fork this repository. 
