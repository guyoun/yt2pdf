# yt2pdf
### Description
YouTube 영상이 변경될 때마다 JPEG 이미지를 캡처하고, 이를 PDF 파일로 병합하는 Python 프로그램

#### 구조
1. yt-dlp를 사용하여 영상을 다운로드
2. scenedetect를 사용하여 영상 내용이 변경하는 타임 스탬프를 검색
3. 검색된 타임스탬프에 해당하는 프레임을 JPG로 저장
4. JPG를 PDF로 병합

### Requirements
```
opencv-python==4.7.0.72
Pillow==9.5.0
pycryptodomex==3.17
pypdf==3.8.1
scenedetect==0.6.1
yt-dlp==2023.3.4
```

### Usage
1. 라이브러리 설치
```
pip install -r requirements.txt
```

2. 프로그램 실행
```
python main.py [YouTube URL]
```

3. 실행한 경로에 output.pdf로 저장 됨