from app import App

app = App(port=10203)
app.setup_server()
app.setup_pose_estimator()
app.capture_and_broadcast_pose()
app.close_server()
