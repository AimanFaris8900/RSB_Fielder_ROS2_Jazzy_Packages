import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/rsbdev/ros2_ws/src/fielder_navigation/install/fielder_navigation'
