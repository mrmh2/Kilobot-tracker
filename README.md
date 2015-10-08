# Kilobot tracking code

Code for tracking Kilobots from videos.

To unpack a mp4:

    ffmpeg -i follow-fast.mp4 -r 1 leader/follow%04d.png
