from typing import Callable, Optional
import pyarrow as pa
from dora import DoraStatus
import dora
import numpy as np
import time
class Operator:
    def __init__(self) -> None:
        self.ros2_context = dora.Ros2Context()
        # create ros2 node
        self.ros2_node = self.ros2_context.new_node(
            "lidar2ros",
            "/ros2_bridge",
            dora.Ros2NodeOptions(rosout=True)
        )
        # create ros2 qos
        self.topic_qos = dora.Ros2QosPolicies(
            reliable=True, max_blocking_time=0.1
        )
        # create ros2 topic
        self.laser_scan_topic = self.ros2_node.create_topic(
            "/ros2_bridge/laser_scan",
            "sensor_msgs::LaserScan",
            self.topic_qos
        )
        # create ros2 publisher
        self.laser_scan_publisher = self.ros2_node.create_publisher(self.laser_scan_topic)
    
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "tick":
            print("tick")
            # 假设数据
            sec = int(time.time())
            nanosec = int((time.time() - sec) * 1e9)
            angle_min = -np.pi / 2  # 最小角度
            angle_max = np.pi / 2   # 最大角度
            angle_increment = np.pi / 180  # 角度增量
            time_increment = 0.01  # 时间增量
            scan_time = 0.1  # 扫描时间
            range_min = 0.2  # 最小距离
            range_max = 10.0  # 最大距离
            ranges = np.random.uniform(range_min, range_max, int((angle_max - angle_min) / angle_increment)).tolist()  # 假设距离数据
            intensities = np.random.uniform(0, 255, len(ranges)).tolist()  # 假设强度数据

            # LaserScan 消息字典
            laser_scan_dict = {
                "header": {
                    "stamp": {
                        "sec": np.int32(sec),
                        "nanosec": np.uint32(nanosec),
                    },
                    "frame_id": "laser_frame",
                },
                "angle_min": angle_min,
                "angle_max": angle_max,
                "angle_increment": angle_increment,
                "time_increment": time_increment,
                "scan_time": scan_time,
                "range_min": range_min,
                "range_max": range_max,
                "ranges": ranges,
                "intensities": intensities,
            }

            print(laser_scan_dict)
            self.laser_scan_publisher.publish(pa.array([laser_scan_dict]))
        return DoraStatus.CONTINUE
