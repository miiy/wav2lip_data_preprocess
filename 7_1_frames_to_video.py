import os
import argparse
import cv2
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Convert frame+audio folders to videos")
    parser.add_argument("--frames_audios_dir", required=True, help="The directory which contains frames and audios", type=str)
    args = parser.parse_args()

    frames_audios_dir = os.path.abspath(args.frames_audios_dir)
    if not os.path.isdir(frames_audios_dir):
        raise ValueError("Please input the path of a valid directory")

    parent_dir = os.path.dirname(frames_audios_dir)
    basename = os.path.basename(frames_audios_dir)
    dst_dir = os.path.join(parent_dir, basename + "_mp4")

    create_videos_from_all_valid_subfolders(frames_audios_dir, dst_dir)

def create_videos_from_all_valid_subfolders(src_root, dst_root):
    for root, dirs, files in os.walk(src_root):
        # 判断当前目录是否符合：至少包含一个 .jpg 和 audio.wav
        has_jpg = any(f.endswith('.jpg') for f in files)
        has_audio = 'audio.wav' in files
        if not (has_jpg and has_audio):
            continue

        print(f"正在处理: {root}")
        # 按照源目录相对路径结构创建输出路径
        rel_path = os.path.relpath(root, src_root)
        output_dir = os.path.join(dst_root, os.path.dirname(rel_path))
        os.makedirs(output_dir, exist_ok=True)
        output_video_path = os.path.join(dst_root, rel_path + ".mp4")

        create_video_from_folder(root, output_video_path)

def create_video_from_folder(folder_path, output_video_path):
    images = sorted([img for img in os.listdir(folder_path) if img.endswith(".jpg")])
    if not images:
        print(f"跳过（无图像）: {folder_path}")
        return

    audio_path = os.path.join(folder_path, "audio.wav")
    if not os.path.exists(audio_path):
        print(f"跳过（无音频）: {folder_path}")
        return

    first_frame = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, layers = first_frame.shape
    size = (width,height)
    temp_video_path = os.path.join(os.path.dirname(output_video_path), "temp_" + os.path.basename(output_video_path))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 25
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, size)

    images = sorted_images(images)

    for image in images:
        frame = cv2.imread(os.path.join(folder_path, image))
        frame = cv2.resize(frame, size)
        out.write(frame)
    out.release()

    cmd = [
        "ffmpeg", "-y",
        "-i", temp_video_path,
        "-i", audio_path,
        "-ar", "16000",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_video_path
    ]
    subprocess.run(cmd, check=True)
    os.remove(temp_video_path)
    print(f"Success: {output_video_path}")


def sorted_images(images):
    # 提取文件名中的数字部分
    def extract_number(filename):
        return ''.join(filter(str.isdigit, filename))

    # 找出文件名中数字部分的最大长度
    max_len = max(len(extract_number(img)) for img in images)
    
    # 补充零并按补充零后的文件名排序
    def pad_number(filename):
        number = extract_number(filename)
        return filename.replace(number, number.zfill(max_len))
    
    # 对文件按补零后的文件名排序
    sorted_images = sorted(images, key=pad_number)
    return sorted_images

if __name__ == '__main__':
    main()
