# wav2lip_data_preprocess

## dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
git clone https://github.com/breizhn/DTLN.git

# 分割视频
python 4_split_videos.py --source_videos_dir ./data/videos

# 转换视频帧率到25fps和音轨16000hz
python 5_convert_25fps_16000hz.py --videos_pieces_dir ./data/videos_pieces

# 分辨率筛选，存图片，降噪，存 mel 频谱
# transform videos to frames and audio
# macos pip install urllib3==1.26.20
python 6_trsf_vds2frs_ads.py --input_videos_dir ./data/videos_pieces
# Downloading: "https://www.adrianbulat.com/downloads/python-fan/3DFAN4-4a694010b9.zip" to /home/ubuntu/.cache/torch/hub/checkpoints/3DFAN4-4a694010b9.zip

# syncnet 同步
python 7_rank_by_syncnet.py --frames_audios_dir ./data/frames_audios/

# 抽样
python 8_sample.py --frames_audios_dir ./data/frames_audios_ranked_by_syncnet/
```
