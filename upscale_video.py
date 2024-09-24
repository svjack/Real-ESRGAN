import argparse
import torch
import cv2
import os
import subprocess

def upscale_video(video_path, output_dir, resolution, model, python_runtime):
    assert torch.cuda.is_available(), "GPU not detected.. Please change runtime to GPU"

    assert os.path.exists(video_path), "Video file does not exist"

    video_capture = cv2.VideoCapture(video_path)
    video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    final_width = None
    final_height = None
    aspect_ratio = float(video_width / video_height)

    # Get output resolutions
    match resolution:
        case "FHD":
            final_width = 1920
            final_height = 1080
        case "2k":
            final_width = 2560
            final_height = 1440
        case "4k":
            final_width = 3840
            final_height = 2160
        case "2x":
            final_width = 2 * video_width
            final_height = 2 * video_height
        case "3x":
            final_width = 3 * video_width
            final_height = 3 * video_height
        case "4x":
            final_width = 4 * video_width
            final_height = 4 * video_height

    if aspect_ratio == 1.0 and "x" not in resolution:
        final_height = final_width

    if aspect_ratio < 1.0 and "x" not in resolution:
        temp = final_width
        final_width = final_height
        final_height = temp

    scale_factor = max(final_width / video_width, final_height / video_height)
    isEven = int(video_width * scale_factor) % 2 == 0 and int(video_height * scale_factor) % 2 == 0

    # scale_factor needs to be even
    while isEven == False:
        scale_factor += 0.01
        isEven = int(video_width * scale_factor) % 2 == 0 and int(video_height * scale_factor) % 2 == 0

    print(f"Upscaling from {video_width}x{video_height} to {final_width}x{final_height}, scale_factor={scale_factor}")

    # Run the inference script with subprocess
    command = [
        python_runtime,
        "inference_realesrgan_video.py",
        "-n", model,
        "-i", video_path,
        "-o", output_dir,
        "--outscale", str(scale_factor)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    video_name_with_ext = os.path.basename(video_path)
    video_name = video_name_with_ext.replace(".mp4", "")
    upscaled_video_path = f"{output_dir}{video_name}_out.mp4"
    final_video_name = f"{video_name}_upscaled_{final_width}_{final_height}.mp4"
    final_video_path = os.path.join(output_dir, final_video_name)

    # crop to fit
    if "x" not in resolution:
        print("Cropping to fit...")
        command = [
            "ffmpeg",
            "-loglevel", "error",
            "-hwaccel", "cuda",
            "-y",
            "-i", upscaled_video_path,
            "-c:v", "h264_nvenc",
            "-filter:v", f"crop={final_width}:{final_height}:(in_w-{final_width})/2:(in_h-{final_height})/2",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            final_video_path
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

    print(f"Upscaled video saved to: {final_video_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upscale a video using Real-ESRGAN")
    parser.add_argument("video_path", type=str, help="Path to the input video file")
    parser.add_argument("-o", "--output_dir", type=str, default=".", help="Directory to save the output video")
    parser.add_argument("-r", "--resolution", type=str, choices=["FHD", "2k", "4k", "2x", "3x", "4x"], default="4k", help="Desired output resolution")
    parser.add_argument("-m", "--model", type=str, choices=["RealESRGAN_x4plus", "RealESRGAN_x4plus_anime_6B", "realesr-animevideov3"], default="RealESRGAN_x4plus", help="Real-ESRGAN model to use")
    parser.add_argument("-p", "--python_runtime", type=str, default="/environment/miniconda3/envs/video_4k/bin/python", help="Path to the Python runtime to use")

    args = parser.parse_args()

    upscale_video(args.video_path, args.output_dir, args.resolution, args.model, args.python_runtime)
