## Pre-requisite
- Install SensorConnect Software on a Windows computer
- Enable magnetometer aid in estimation filter

## Calibration
- Optional: Launch calib_accel node
    ```
    <node ns="$(arg robot_name)" pkg="calib_accelerometer" type="calib_accel" name="accl_calibrator" output="screen">
      <remap from="/imu_input" to="imu/data_raw"/>
      <param name="max_samples" value="1000" />
      <param name="log" value="false" />
    </node> 

    ```
-   calibrate accelerometer
    ```
    rosservice call /alpha_rise/accl_calibrator/start_sampling
    # keep imu steady
    rosservice call /alpha_rise/accl_calibrator/stop_sampling
    rosservice call /alpha_rise/accl_calibrator/calibrate_accl
    ```
- Write down the accelerometer bias

- Open SenseConnect on Windows PC
    - Go to `Device` tab -> `Configure` menu
    - Type in accelerometer bias under `Accelerometer/Gyro Bias section

- In the same place, click `capture gyro bias` tab and have IMU stay steady to obtain the gyro bias.

- Go to `Device` tab -> `Magnetic Calibration` menu
    - Click `start` under `collect data`
    - Rotate your IMU around all three axes.
    - If the spatial coverage has exceeded `95%`, you can click `stop`
    - Then click `Start` under `Verify data`
    - Choose `Ellipsodial Fit` under Device Calibration section.
    - If the soft and hard-iron are reasonable, you can click `write` to store it to the IMU

## Configuration 
- Go back to `Device` tab -> `Configure` menu and turn on the following settings for good EKF filtered IMU data
    - Under `Estimation Filter`, make sure you have selected `Magnetometer aiding` under `aiding source enable`
    - Under `IMU-AHRS` Section, Make sure you selected `Enable up compensation` and `Enable North Compensation`
    - Under `Low-pass filter Settings` make sure you have applied all the filters.
- Go to `Device` tab -> `Save/load Settings`
    - CLick `Save as startup settings` such that all configurations are stored on the AHRS..

- `Reboot device`

- Recheck the settings under `Configure` make sure they are stored.

- Also go to `Status QuickView` to make sure Magnetometer is enabled and used in `aiding measurements`

## Test

- Now, we will use the new microstrain driver.
    ```
    roslaunch alpha_rise_bringup test_microstrain.launch
    ```

- You need to use the filtred data `/ns/ekf/imu/data`