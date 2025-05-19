cmake_minimum_required(VERSION 3.8)
project(alpha_rise_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rviz2 REQUIRED)
find_package(tf2_ros REQUIRED)

install(DIRECTORY 
  mesh
  urdf 
  # config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()