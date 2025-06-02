cmake_minimum_required(VERSION 3.8)
project(alpha_rise_config)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
# find_package(rviz2 REQUIRED)
# find_package(tf2_ros REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.

install(DIRECTORY 
  mvp_control_config
  mvp_mission_config
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()