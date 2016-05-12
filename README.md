Sean Quinn (spq@case.edu)
May 8 2016

This script reads timing data from slimtim. Messages are sent over a serial
connection (9600 bps) in ASCII text.

# 1. DEPENDENCIES/REQUIRED SOFTWARE

This is a Python 2 program. The only dependency is Python 2.7+

In this version, only Python built-in modules are used.

# 2. INPUT DATA

A USB-serial adapter is used to receive data from slimtim. The OS presents this
as a symbolic link in ```/dev/```, usually in the order the adapters were
conneccted, such as ```/dev/ttyUSB0```.

## 2.1 Serial console settings (IMPORTANT!)

Since slimtim is sending at 9600 and has some other quirks it is crucial
the symbolic link be configured correctly! Generally the default bitrate is
9600, however, we also want to ignore carriage returns. Use the program
```stty``` to do this. It can be invoked as ```stty -F /dev/ttyUSB0 [options]```
The following tty settings have been used on testing machines in the
lab with success

```
speed 9600 baud; rows 0; columns 0; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>;
eol2 = <undef>; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R;
werase = ^W; lnext = ^V; flush = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 hupcl -cstopb cread clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr igncr -icrnl ixon -ixoff
-iuclc -ixany -imaxbel -iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt
echoctl echoke
```

Aside from enabling ignore carriage returns, these are mostly defaults.

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