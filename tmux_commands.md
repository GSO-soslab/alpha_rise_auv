# Tmux Commands
Tmux allows to have a terminal session inside the host machine such that even if the connection is lost, the session is not interrupted.

## Commands

```tmux new -s <name>``` to create a tmux terminal with a name<br>

```Ctrl+b, d``` to exit the tmux terminal.

```tmux ls``` to view all the tmux sessions. <br>

```tmux attach -t <name>``` to enter the tmux terminal of choice.

```Ctrl+b,[``` to enable navigation mode. Note this stops the std buffer printouts. <br>
Press `q` to exit the navigation mode.
## Run
```ros2 launch alpha_rise_bringup bringup_vehicle_c2.launch.py``` inside the tmux terminal.