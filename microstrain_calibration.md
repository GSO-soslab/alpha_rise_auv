## Pre-requisite
- Download `ROS_MSCL`, this has services to set the imu bias
    ```
    git clone https://github.com/GSO-soslab/ROS_MSCL
    ```
- follow the instruction there to install the `mscl.deb` file under dependency (Note: choose the one that is compatible with your computer).

- Download microstrain-inertial-driver which is used for final testing
    ```
    sudo apt install ros-noetic-microstrain-inertial-driver
    ```

## Calibration
- launch the ROS_MSCL driver
    ```
    roslaunch alpha_rise_bringup calibration_microstrain.launch
    ```

- make sure `save_settings` parameter in the launch file is set to true so your setting can be saved.

- save original bias setting
    ```
    rosservice call /alpha_rise/get_accel_bias

    rosservice call /alpha_rise/get_gyro_bias

    rosservice call /alpha_rise/get_hard_iron_values

    rosservice call /alpha_rise/get_soft_iron_matrix
    ```

- clear all bias param in the IMU

    ```
    rosservice call /alpha_rise/set_accel_bias  [to 0.0, 0.0, 0.0]
    rosservice call /alpha_rise/set_gyro_bias  [to 0.0, 0.0, 0.0]
    rosservice call /alpha_rise/set_hard_iron_values [to 0.0, 0.0, 0.0]
    rosservice call /alpha_rise/set_soft_iron_matrix [to 1.0, 0.0, 0,0; 0.0, 1.0, 0.0; 0.0, 0.0, 1.0];
    ```

- calibrate accelerometer
    ```
    rosservice call /alpha_rise/accl_calibrator/start_sampling
    # keep imu steady
    rosservice call /alpha_rise/accl_calibrator/stop_sampling
    rosservice call /alpha_rise/accl_calibrator/calibrate_accl
    ```
- calibrate gyro
    ```
    rosservice call /alpha_rise/gyro_calibrator/start_sampling
    #keey imu steady
    rosservice call /alpha_rise/gyro_calibrator/stop_sampling
    ```
    - The gyro bias is printed in the terminal

- calibrate magnetometer 
   - option:1
        - record a rosbag while you are rotating imu in all direction.
        - run matlab script under `alpha_rise_config/sh`

    - option: 2
        ```
        rosservice call /alpha_rise/mag_calibrator/start_sampling
        # rotate imu in all directions
        rosservice call /alpha_rise/mag_calibrator/stop_sampling
        rosservice call /alpha_rise/mag_calibrator/calibrate_mag
        ```
        - bias and soft-iron matrix will print in the terminal
        - note: the software will only show the upper part, and you can fill the zero elements.
    We tested both options, and also left zeros in the lower part in option2. All yield similar results.
        


- set all bias param in the IMU in terminal with the following services

    ```
    rosservice call /alpha_rise/set_accel_bias 
    rosservice call /alpha_rise/set_gyro_bias  
    rosservice call /alpha_rise/set_hard_iron_values 
    rosservice call /alpha_rise/set_soft_iron_matrix
    ```
    - wait for at least 20 seconds for the configuration to be set to the memory.
    - make sure `device_setup` is set to `true` in `microstrain_mscl.launch.xml`
- You can replug the microstrain back in and run the driver and make sure the params are saved by calling get_xx_bias services.

## Test

- Now, we will use the new microstrain driver.
    ```
    roslaunch alpha_rise_bringup test_microstrain.launch
    ```

- You need to use the filtred data `/ns/ekf/imu/data`