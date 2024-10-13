import pyrealsense2 as rs
import numpy as np
import cv2

class DepthCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.profile = self.pipeline.start(config)

        # To align depth and color frame
        align_to = rs.stream.color
        self.align = rs.align(align_to)        

        # flag
        self.flag = True        

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()

        aligned_frames = self.align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            return False, None, None, None, None  

        temp_filter = rs.temporal_filter()
        # hole_filling = rs.hole_filling_filter()
        depth_frame = temp_filter.process(depth_frame)
        # depth_frame = hole_filling.process(depth_frame)

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        # Create colormap to show the depth of the Objects
        # colorizer = rs.colorizer()
        # depth_colormap = np.asanyarray(colorizer.colorize(depth_image).get_data()) 

        # Get camera intrinsics
        intr_ = self.profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
        intr = [intr_.ppx, intr_.ppy, intr_.fx, intr_.fy]      

        return True, depth_image, color_image, depth_colormap, intr

    def release(self):
        self.pipeline.stop()

    def isOpened(self):
        if self.flag:
            return True
        else:
            return False
