# ARTutor
This project aims to develop a Unity AR application that leverages
MediaPipe as the body tracking package in Python. The application incorporates
buffer queues and multithreading to enhance the efficiency and real-time
interaction of the system. The body tracking process begins with MediaPipe,
which provides models for accurate body pose estimation. The tracked data
undergoes processing and analysis in Python, and is broken into chunks and
broadcasted with delimiters. On the receiving side, a UDP packet receiver
thread, written in C# , receives the key point landmarks of the tracked human
and stores the chunks in a buffer queue and assembles them and converts the
assembled chunks back into keypoint-landmarks in a separate thread and
forwards it to the keypoint mapper function which takes care of mapping the
coordinates with 3d Character. The Unity AR Foundation Package coupled with
AR Core library takes care of augmenting the character in the real environment
where learners can observe and interact with a humanoid avatar representing the
performers's movements. The integration of buffer queues and multithreading
improves synchronization, data flow, and performance, creating an immersive
and interactive learning experience. The proposed system addresses the
limitations of traditional teaching methods by providing an engaging and
realistic virtual learning environment. By utilizing MediaPipe for body tracking,
Python for data processing, sockets for real-time communication, and Unity for
AR application development, this project presents a comprehensive solution that
enables learners to visualize and mimic the performer's movements in a
dynamic and interactive manner.
<br>
[Click For full Documentation](https://github.com/Aadityaprabu002/ARTutor/blob/main/Documentation/ARTUTOR.pdf)
<br>
[Click here for demo](https://youtube.com/playlist?list=PLCk1Y31wvMhXjcgWnek1wSJLmZKr1x8f1)
