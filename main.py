import zmq
import sys
import numpy as np
import msgpack

# establish ZMQ context
ctx = zmq.Context()
# The REQ talks to Pupil remote and receives the session unique IPC SUB PORT
pupil_remote = ctx.socket(zmq.REQ)

ip = 'localhost'  # If you talk to a different machine use its IP.
port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.

# connect to Pupil Capture
pupil_remote.connect(f'tcp://{ip}:{port}')

# Request 'SUB_PORT' for reading data
pupil_remote.send_string('SUB_PORT')
sub_port = pupil_remote.recv_string()

# Request 'PUB_PORT' for writing data
# pupil_remote.send_string('PUB_PORT')
# pub_port = pupil_remote.recv_string()


subscriber = ctx.socket(zmq.SUB)
subscriber.connect(f'tcp://{ip}:{sub_port}')
subscriber.subscribe('gaze.3d.0')  # receive all gaze messages

while True:
    topic, payload = subscriber.recv_multipart()
    message = msgpack.loads(payload)
    eye_center_3d = np.array(message[b'eye_center_3d'])
    gaze_point_3d = np.array(message[b'gaze_point_3d'])
    gaze_normal_3d = np.array(message[b'gaze_normal_3d'])
    d = gaze_point_3d - eye_center_3d
    norm = np.linalg.norm(d, 2)
    print(f'Gaze vector: {d}')
    print(f'Length of gaze vector: {norm}')
    

