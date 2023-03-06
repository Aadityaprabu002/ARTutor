from app import App

app = App()
app.setup_server()
app.setup_pose_estimator()
print('Server Started')
print('Pose Capture starting...')
app.capture_and_broadcast_pose()
print('Pose Capture ended!')
app.close_server()
