
from sensor_streamer_handlers.SensorManager import SensorManager

import time
import os
import traceback
from utils.time_utils import *
from utils.print_utils import *

# Note that multiprocessing requires the __main__ check.
if __name__ == '__main__':
  # Configure printing and logging.
  print_status = True
  print_debug = False
  
  # Helper methods for logging/printing.
  def _log_status(msg, *extra_msgs, **kwargs):
    write_log_message(msg, *extra_msgs, source_tag='launcher',
                      print_message=print_status, filepath=log_history_filepath, **kwargs)
  def _log_debug(msg, *extra_msgs, **kwargs):
    write_log_message(msg, *extra_msgs, source_tag='launcher',
                      print_message=print_debug, debug=True, filepath=log_history_filepath, **kwargs)
  def _log_error(msg, *extra_msgs, **kwargs):
    write_log_message(msg, *extra_msgs, source_tag='launcher',
                      print_message=True, error=True, filepath=log_history_filepath, **kwargs)
  def _log_warn(msg, *extra_msgs, **kwargs):
    write_log_message(msg, *extra_msgs, source_tag='launcher',
                      print_message=True, warning=True, filepath=log_history_filepath, **kwargs)
  def _log_userAction(msg, *extra_msgs, **kwargs):
    write_log_message(msg, *extra_msgs, source_tag='launcher',
                      print_message=True, userAction=True, filepath=log_history_filepath, **kwargs)
  
  # Define the streamers to use.
  sensor_streamer_specs = [
    # # Allow the experimenter to label data and enter notes.
    # {'class': 'ExperimentControlStreamer',
    #  'print_debug': print_debug, 'print_status': print_status
    #  },
    # Allow the experimenter to record timestamped notes at any time.
    {'class': 'NotesStreamer',
     'print_debug': print_debug, 'print_status': print_status
     },
    # # Stream from the Myo device including EMG, IMU, and gestures.
    # {'class': 'MyoStreamer',
    #  'num_myos': 2,
    #  'print_debug': print_debug, 'print_status': print_status
    #  },
    # # Stream from the Xsens body tracking and Manus gloves.
    # {'class': 'XsensStreamer',
    #  'print_debug': print_debug, 'print_status': print_status
    #  },
    # Stream from one or more tactile sensors, such as the ones on the gloves.
    # See the __init__ method of TouchStreamer to configure settings such as
    #  what sensors are available and their COM ports.
    {'class': 'TouchStreamer',
     'print_debug': print_debug, 'print_status': print_status
     },
    # # Stream from the Pupil Labs eye tracker, including gaze and video data.
    # {'class': 'EyeStreamer',
    #  'stream_video_world'    : False, # the world video
    #  'stream_video_worldGaze': True, # the world video with gaze indication overlayed
    #  'stream_video_eye'      : False, # video of the eye
    #  'print_debug': print_debug, 'print_status': print_status
    #  },
    # # Stream from the Dymo M25 scale.
    # {'class': 'ScaleStreamer',
    #  'print_debug': print_debug, 'print_status': print_status
    #  },
    # # Stream from one or more microphones.
    # {'class': 'MicrophoneStreamer',
    #  'device_names_withAudioKeywords': {'microphone_conference': 'USB audio CODEC'},
    #  'print_debug': print_debug, 'print_status': print_status
    #  },
    # # Dummy data.
    # {'class': 'DummyStreamer',
    #  'update_period_s': 0.1,
    #  'print_debug': print_debug, 'print_status': print_status
    #  },
  ]
  
  # Configure where and how to save sensor data.
  # To not log data, simply set
  datalogging_options = None
  log_dir = None
  log_history_filepath = None
  # script_dir = os.path.dirname(os.path.realpath(__file__))
  # (log_time_str, log_time_s) = get_time_str(return_time_s=True)
  # log_tag = 'testing-tactiles'
  # log_dir_root = os.path.join(script_dir, '..', 'data', '%s_test_tactile_sensors' % get_time_str(format='%Y-%m-%d'))
  # log_subdir = '%s_%s' % (log_time_str, log_tag)
  # log_dir = os.path.join(log_dir_root, log_subdir)
  # datalogging_options = {
  #   'log_dir': log_dir, 'log_tag': log_tag,
  #   'use_external_recording_sources': True,
  #   'videos_in_hdf5': False,
  #   'audio_in_hdf5': False,
  #   # Choose whether to periodically write data to files.
  #   'stream_csv'  : False,
  #   'stream_hdf5' : True,
  #   'stream_video': True,
  #   'stream_audio': True,
  #   'stream_period_s': 15,
  #   'clear_logged_data_from_memory': True, # ignored if dumping is also enabled
  #   # Choose whether to write all data at the end.
  #   'dump_csv'  : False,
  #   'dump_hdf5' : False,
  #   'dump_video': False,
  #   'dump_audio': False,
  #   # Additional configuration.
  #   'videos_format': 'avi', # mp4 occasionally gets openCV errors about a tag not being supported?
  #   'audio_format' : 'wav', # currently only supports WAV
  #   'print_status': print_status, 'print_debug': print_debug
  # }
  # # Initialize a file for writing the log history of all printouts/messages.
  # log_history_filepath = os.path.join(log_dir, '%s_log_history.txt' % log_time_str)
  # os.makedirs(log_dir, exist_ok=True)
  
  # Configure visualization.
  # To not show any visualizations, simply set
  # visualization_options = None
  composite_frame_size = (900, 1500) # height, width # (1800, 3000)
  composite_col_width = int(composite_frame_size[1]/3)
  composite_row_height = int(composite_frame_size[0]/3)
  visualization_options = {
    'visualize_streaming_data'       : True,
    'visualize_all_data_when_stopped': False,
    'wait_while_visualization_windows_open': False,
    'update_period_s': 0.4,
    # 'classes_to_visualize': ['TouchStreamer']
    'use_composite_video': False, # If False, each streamer will spawn its own visualization window
    # 'composite_video_layout': [
    #   [
    #     {'device_name':'dummy-line', 'stream_name':'dummy-stream', 'width':1500, 'height':1500},
    #     {'device_name':'dummy-line', 'stream_name':'dummy-stream', 'width':1500, 'height':750},
    #   ],
    #   [
    #     {'device_name':None, 'stream_name':None, 'width':0, 'height':0},
    #     {'device_name':'dummy-line', 'stream_name':'dummy-stream', 'width':1500, 'height':750},
    #   ],
    # ],
    'composite_video_layout':
      [
        [ # row 0
          {'device_name':'tactile-glove-left', 'stream_name':'tactile_data',    'rowspan':1, 'colspan':1, 'width':composite_col_width, 'height':composite_row_height},
          {'device_name':'tactile-glove-right', 'stream_name':'tactile_data',   'rowspan':1, 'colspan':1, 'width':composite_col_width, 'height':composite_row_height},
        ],
      ],
  }
  if log_dir is not None:
    visualization_options['composite_video_filepath'] = os.path.join(log_dir, 'composite_visualization')
  
  # Create a sensor manager.
  sensor_manager = SensorManager(sensor_streamer_specs=sensor_streamer_specs,
                                 data_logger_options=datalogging_options,
                                 data_visualizer_options=visualization_options,
                                 print_status=print_status, print_debug=print_debug,
                                 log_history_filepath=log_history_filepath)
  
  # Define a callback to print FPS for a certain device.
  # print_fps = False # Use this to disable FPS printing
  classes_to_exclude_for_fps = ['ExperimentControlStreamer', 'NotesStreamer']
  streamers_for_fps = sensor_manager.get_streamers(class_name=None)
  streamers_for_fps = [streamer for streamer in streamers_for_fps if True not in [exclude in type(streamer).__name__ for exclude in classes_to_exclude_for_fps]]
  fps_start_time_s = [None]*len(streamers_for_fps)
  fps_start_num_timesteps = [0]*len(streamers_for_fps)
  fps_num_timesteps = [0]*len(streamers_for_fps)
  fps_last_print_time_s = 0
  def print_fps():
    global fps_start_time_s, fps_last_print_time_s, fps_start_num_timesteps, fps_num_timesteps
    printed_fps = False
    for (streamer_index, streamer) in enumerate(streamers_for_fps):
      if len(streamer.get_device_names()) == 0:
        continue
      device_for_fps = streamer.get_device_names()[0]
      stream_for_fps = streamer.get_stream_names(device_for_fps)[0]
      num_timesteps = streamer.get_num_timesteps(device_for_fps, stream_for_fps)
      if fps_start_time_s[streamer_index] is None or num_timesteps < fps_num_timesteps[streamer_index]:
        fps_start_time_s[streamer_index] = time.time()
        fps_start_num_timesteps[streamer_index] = num_timesteps
        fps_num_timesteps[streamer_index] = num_timesteps - fps_start_num_timesteps[streamer_index]
        fps_last_print_time_s = time.time()
      elif time.time() - fps_last_print_time_s > 5:
        printed_fps = True
        fps_duration_s = time.time() - fps_start_time_s[streamer_index]
        fps_num_timesteps[streamer_index] = num_timesteps - fps_start_num_timesteps[streamer_index]
        _log_status('Status: %5.1f Hz (%4d timesteps in %6.2fs) for %s: %s' %
                    ((fps_num_timesteps[streamer_index]-1)/fps_duration_s,
                     fps_num_timesteps[streamer_index], fps_duration_s,
                     device_for_fps, stream_for_fps))
    if printed_fps:
      fps_last_print_time_s = time.time()
  
  # Define a callback that checks whether the user has entered a quit keyword.
  try:
    control_streamer = sensor_manager.get_streamers(class_name='ExperimentControlStreamer')[0]
    def check_if_user_quit():
      if callable(print_fps):
        print_fps()
      return not control_streamer.experiment_is_running()
  except:
    try:
      notes_streamer = sensor_manager.get_streamers(class_name='NotesStreamer')[0]
      def check_if_user_quit():
        last_notes = notes_streamer.get_last_notes()
        if last_notes is not None:
          last_notes = last_notes.lower().strip()
        if callable(print_fps):
          print_fps()
        return last_notes in ['quit', 'q']
    except:
      def check_if_user_quit():
        return False
  
  
  # print()
  # print('Enter \'quit\' or \'q\' as an experiment note to end the program')
  # print()
  
  # Run!
  sensor_manager.connect()
  sensor_manager.run(duration_s=36000, stopping_condition_fn=check_if_user_quit)
  sensor_manager.stop()



