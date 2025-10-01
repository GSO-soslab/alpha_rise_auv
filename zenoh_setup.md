# Setting up Zenoh as DDS for multi-machine communication.

## Pre-requisite
```sudo apt-get install ros-jazzy-rmw-zenoh-cpp```

## Setup
In both the devices, go to <br>
```/opt/ros/jazzy/share/rmw_zenoh_cpp/config/DEFAULT_RMW_ZENOH_ROUTER_CONFIG.json5```
<br>

Add other devices' IP & protocol after Line 43<br>
```// "<proto>/<address>"```<br>
```"tcp/IP_OTHER_DEVICE:7447```

Add the following line to .bashrc<br>
```export RMW_IMPLEMENTATION=rmw_zenoh_cpp```

Reboot

## Test
Both the devices should be running 
```ros2 run rmw_zenoh_cpp rmw_zenohd```
to enable the communication.

Test to see if each device can see its own topics/msgs and each others.
