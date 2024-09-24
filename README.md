# Video Upscaling with Real-ESRGAN

## Introduction

This project provides a command-line tool to upscale videos using the Real-ESRGAN model. The tool allows you to upscale videos to various resolutions, including 4K, and crop them to fit the desired aspect ratio. This is particularly useful for enhancing the quality of videos, especially for high-resolution displays.

## Project Overview

The Real-ESRGAN model is a powerful tool for enhancing the resolution of images and videos. This project leverages this model to upscale videos to higher resolutions, such as 4K, while maintaining the aspect ratio and quality of the original video. The tool is designed to be flexible, allowing users to choose different models and resolutions based on their needs.

## Installation

To set up the environment and install the necessary dependencies, follow these steps:

1. **Update and install dependencies**:
   ```bash
   sudo apt-get update && sudo apt-get install ffmpeg git-lfs -y
   pip uninstall requests -y && pip install requests
   ```

2. **Create and activate a Conda environment**:
   ```bash
   conda create --name video_4k python=3.10 -y
   conda activate video_4k
   pip install ipykernel
   python -m ipykernel install --user --name video_4k --display-name video_4k
   ```

3. **Clone the Real-ESRGAN repository and install dependencies**:
   ```bash
   git clone https://huggingface.co/svjack/Real-ESRGAN
   cd Real-ESRGAN
   tar -zxvf Real-ESRGAN.tar.gz
   cd Real-ESRGAN
   pip install torch torchvision
   pip install basicsr facexlib gfpgan ffmpeg ffmpeg-python
   pip install -r requirements.txt
   python setup.py develop
   pip install torchvision==0.15.2
   pip install numpy==1.26.4
   ```

## Command Line Usage

To use the script from the command line, you can run the following command:

```bash
python upscale_video.py <video_path> -o <output_dir> -r <resolution> -m <model> -p <python_runtime>
```

### Example

```bash
python upscale_video.py "1.mp4" -o ./output -r FHD -m RealESRGAN_x4plus -p /environment/miniconda3/envs/video_4k/bin/python
```

### Parameters

- `video_path`: Path to the input video file.
- `-o, --output_dir`: Directory to save the output video (default is the current directory).
- `-r, --resolution`: Desired output resolution (choices: "FHD", "2k", "4k", "2x", "3x", "4x"; default is "4k").
- `-m, --model`: Real-ESRGAN model to use (choices: "RealESRGAN_x4plus", "RealESRGAN_x4plus_anime_6B", "realesr-animevideov3"; default is "RealESRGAN_x4plus").
- `-p, --python_runtime`: Path to the Python runtime to use (default is `/environment/miniconda3/envs/video_4k/bin/python`).

## Notes

- Ensure that you have a GPU available for faster processing.
- The script uses `ffmpeg` for video processing, so make sure it is installed.
- The script supports various output resolutions, including 4K and multiples of the original resolution.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
