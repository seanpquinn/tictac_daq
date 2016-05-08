Sean Quinn (spq@case.edu)
May 8 2016

This script reads timing data from slimtim. Messages are sent over a serial
connection (9600 bps) in ASCII text.

# 1. DEPENDENCIES/REQUIRED SOFTWARE

This is a Python 2 program. The only dependency is Python 2.7+

In this version, only Python built-in modules are used.

# 2. INPUT DATA

A USB-serial adapter is used to receive data from slimtim. The OS presents this
as a file object in ```/dev/```, usually in the order the adapters were
conneccted, such as ```/dev/ttyUSB0```.

In testing (on Ubuntu system) I've found that the driver (Prolific)/OS 
interprets the endl character in each message as \n\n. Python's
```readline''' function parses these as separate strings. A hack is used to
deal with this behavior: only strings larger than  1 byte are analyzed by the
code.

# 3. INSTALLATION

Run the script from any directory.

# 4. EXECUTING PROGRAM

```
python slimtim_daq.py
```

# 5. OUTPUT DATA

Two files are generated and updated as long as the program runs. The first is
```tic_tac_events.txt``` which is a verbatim copy of all serial messages
received from TICTaC apparatus at the SBC.

The second, ```tic_tac.log''' lists the GPS timestamp in GPS_SEC.microsecond
format for all 4 fold coincidence events. These events will be forwared
to Ricardo's SU emulator program to issue a T3 to the south station.

# 6 TO DO

 - Add line to issue T3 request

# 7 CHANGELOG
 - May 8 2016: Initial program uploaded. Basic functionality.