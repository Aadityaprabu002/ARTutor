import mediapipe as mp

mp_pose = mp.solutions.pose
for lm in mp_pose.PoseLandmark:
    print(lm,lm.value,lm.name)