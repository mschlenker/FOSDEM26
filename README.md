# MicroPython on ESP32 – fun with sensors

MicroPython on ESP32 is a very convenient way of working with Microcontroller boards.
For FOSDEM 2026 (and OSMC 2025), we have prepared some examples working with ESP32-C3 Supermini boards.
These have a single-core RISC-V core and are the cheapest available boards at this time, since no royalties for the processing core have to be paid.
If you need more ports and more processing power, look out for Lolin/Wemos S2 Mini or ESP32-S3 boards.

## Download MicroPython

Skip if you have received a board from us at FOSDEM or another event.

The [download page of MicroPython](https://micropython.org/download/) links to all download images and install instructions.
In case your S2/S3 came with a UF2 boot loader, you might use the UF2 images, copy them to the emulated USB flash drive, and call it a day.

For everything else, you need `esptool` or `esptool.py`, either from your distributions repository or installed with the command `pip3 install esptool`.

## Access the board

Once MicroPython is installed, you can access the board using any serial client.
You might use PuTTY or Arduino's serial monitor or some fancy browser running Web-USB client.
I prefer `screen`.
The baud rate of MicroPython usually is 115200.
Once logged on, you can play around in the Python prompt.
If no prompt is shown, press `Ctrl + C`.

```
>>> help();
Welcome to MicroPython on the ESP32!

For online docs please visit http://docs.micropython.org/

For access to the hardware use the 'machine' module:

import machine
pin12 = machine.Pin(12, machine.Pin.OUT)
pin12.value(1)
pin13 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
print(pin13.value())
i2c = machine.I2C(scl=machine.Pin(21), sda=machine.Pin(22))
i2c.scan()
i2c.writeto(addr, b'1234')
i2c.readfrom(addr, 4)

Basic WiFi configuration:

import network
sta_if = network.WLAN(network.WLAN.IF_STA); sta_if.active(True)
sta_if.scan()                             # Scan for available access points
sta_if.connect("<AP_name>", "<password>") # Connect to an AP
sta_if.isconnected()                      # Check for successful connection

Control commands:
  CTRL-A        -- on a blank line, enter raw REPL mode
  CTRL-B        -- on a blank line, enter normal REPL mode
  CTRL-C        -- interrupt a running program
  CTRL-D        -- on a blank line, do a soft reset of the board
  CTRL-E        -- on a blank line, enter paste mode

For further help on a specific object, type help(obj)
For a list of available modules, type help('modules')
>>>
```

We already explained `Ctrl + C`.
Use `Ctrl + D` to exit the interactive prompt and do a soft reboot, effectively starting `main.py`.
If `main.py` prints to STDOUT or STDERR, it will be shown here.
If `main.py` crashes, the stacktrace will be shown here for easy debugging.

To upload programs, I prefer [rshell](https://github.com/dhylands/rshell).
It can be installed from your distributions repository or using `pip3 install rshell`.
This offers a FTP like interface for uploading and downloading files on the MicroPython device.
The Microcontroller board defaults to the "Mountpoint" `/pyboard`.
This can be changed, see the rshell documentation on GitHub.

### Listing all files

```
mattias@barium:/tmp$ rshell -p /dev/ttyACM0 ls /pyboard
Using buffer-size of 32
Connecting to /dev/ttyACM2 (buffer-size 32)...
Trying to connect to REPL  connected
Retrieving sysname ... esp32
Testing if ubinascii.unhexlify exists ... Y
Retrieving root directories ... /boot.py/ /main.py/ /secrets.py/
Setting time ... Jan 31, 2026 08:23:03
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 2000
boot.py    main.py    secrets.py
```

### Show the content of a file

```
mattias@barium:/tmp$ rshell -p /dev/ttyACM0 cat /pyboard/secrets.py
Using buffer-size of 32
Connecting to /dev/ttyACM2 (buffer-size 32)...
Trying to connect to REPL  connected
Retrieving sysname ... esp32
Testing if ubinascii.unhexlify exists ... Y
Retrieving root directories ... /boot.py/ /main.py/ /secrets.py/
Setting time ... Jan 31, 2026 08:46:03
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 2000
secrets = {
    'ssid' : 'your_ssid',
    'wpapsk' : 'T0p_S3cr37_PSK'
}
```

### Upload a file

```
mattias@barium:/tmp$ rshell -p /dev/ttyACM0 cp /home/mattias/main.py /pyboard/main.py
Using buffer-size of 32
Connecting to /dev/ttyACM2 (buffer-size 32)...
Trying to connect to REPL  connected
Retrieving sysname ... esp32
Testing if ubinascii.unhexlify exists ... Y
Retrieving root directories ... /boot.py/ /main.py/ /secrets.py/
Setting time ... Jan 31, 2026 08:52:03
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 2000
Copying '/home/mattias/main.py' to '/pyboard/main.py' ...
```

## Scripts we prepared!

We prepared some scripts to interact with the soil moisture sensors we gave away at FOSDEM 2026 and that I already mentioned in my OSMC 2025 talk.

### Just testing

The script `justsensor/main.py` just loops over the capacative soil moisture sensor and prints the values each two seconds.
For totally dry, it should print out around 4000, for submerging in water around 1200.

### A minimal Checkmk agent

This provides a minimal Checkmk agent output on port 6556, looking like this:

```
<<<check_mk_agent>>>
AgentOS: MicroPython
<<<soilmoisture>>>
1596
<<<local>>>
0 "Soil moisture ESP32" smval=1596 Everything is fine
```

There are three sections.
First, the Checkmk agent, it just has to be there and hint on the operating system.
Second, a section for a [plug-in](https://docs.checkmk.com/latest/en/devel_check_plugins.html) subscribing to this.
Third, a [local check](https://docs.checkmk.com/latest/en/localchecks.html), with the state calculated locally on the sensor board.

### Prometheus scraping endpoint

This uses [Prometheus express](https://github.com/ssube/prometheus_express) stolen from ssube and verbatim copied.
Please check out their repository in case of updates.
The example code reads the on-die temperature sensor of the ESP32.

### Syslog UDP sender

Another example, that shamelessly steals from other people's work.
It uses [Usyslog from kfricke](https://github.com/kfricke/micropython-usyslog).
This example expects a "door open sensor", aka microswitch, connected to 39 (I did this example on S2), so change ports.
Values are sent to some UDP syslog receiver.

The most smart part about this is how easily the microcontroller can be told to sleep for a few minutes, before waking up, sleeping and so on...

## 3D printed enclosure

The enclosure consists of four parts: two inner T shaped parts that hold sensor and ESP32-C3 together and then slide into the lower part of the outer casing.
This is then closed with a smaller upper cover.
I printed the T shaped parts with brim.
For the outer casing, no brim is necessary.
Because of the tight tolerances, you might need to sand the T shaped parts until everything fits.

To bolt the casing together, use 2.5x20 to 3x30 wood screws, like [Heco Topix](https://www.heco-schrauben.com/HECO-TOPIX-plus-3.5-x-30-countersunk-head-HD-20-TG-A3K-1000-pieces/60261) or similar.

