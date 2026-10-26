
# Changelog - Scientific Lineage

## V4 - 2026-10-26 19:17
- Tech: cv2.VideoCapture(rtsp://.../Streaming/Channels/102) + 1MB buffer
- Error: h264 too many ref frames 18, non-existing PPS
- Status: FAILED
- Learning: OpenCV bundled FFmpeg too old for Hikvision High Profile

## V5 - 2026-10-26 20:08
- Tech: requests.get(ISAPI/Streaming/channels/102/picture)
- Error: ModuleNotFoundError: No module named 'requests'
- Status: CRASH on user PC
- Learning: Client PC has no pip libs, use stdlib only

## V5b - 2026-10-26 20:11
- Tech: urllib.request + Basic Auth + ISAPI picture
- Success: Live! Frame 129 - 12KB - 100% Clear - No H264 errors!
- Status: SUCCESS SD 480p
- Learning: Built-in libs win, JPEG bypasses H264 entirely

## V5c - 2026-10-26 20:16
- Tech: V5b + Channel 101 (Main Stream)
- Success: 1080p Full HD
- Status: SUCCESS HD
- Learning: 101 = HD 1920x1080, 102 = SD 640x480

## V6 Ultimate - 2026-10-26 20:23
- Tech: V5c + Face/Human/Vehicle Detection + Playback tab + Save
- Success: PLAYBACK! Frame 233 - 13KB 1080p Clear - FaceON HumanON VehicleON
- Status: ULTIMATE
- Learning: Add features only after core is 100% stable
