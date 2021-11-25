# Controlling PC volume using hand gesture

## Modules used
- opencv
- mediapipe
- time

## How it works

- `while true` loop is counting each itration of frames
- Using mediapipe we are getting position of all hand joins of each frame
- After calcutating difference we are setting the volume of pc