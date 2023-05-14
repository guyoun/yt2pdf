#!/usr/bin/env python

import subprocess as sp
import cv2
import os
import shutil
import io
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

def prepare_output(image_dir):

    if os.path.exists('output.pdf'):
        os.remove('output.pdf')

    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)
    os.makedirs(image_dir)


def download_vide(url):
    # download video
    # yt-dlp -f 'bestvideo[ext=mp4]' -o 'video.%(ext)s' URL
    sp.check_call(['yt-dlp', '-f', 'bestvideo[ext=mp4]', '-o', 'video.%(ext)s', '--force-overwrites', url])


# 씬 감지를 위한 함수
def detect_scenes(video_path, threshold):
    # 비디오 매니저 생성
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    # 비디오 매니저 및 씬 매니저 실행
    try:
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list()
    except Exception:
        scene_list = []

    return scene_list


# 프레임 추출을 위한 함수
def extract_frames(video_path, scene_list, image_dir):
    # 영상 파일 읽기
    cap = cv2.VideoCapture(video_path)

    for scene in scene_list:
        start_timecode = scene[0]
        frame_number = start_timecode.get_frames()
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = cap.read()
        if ret:
            filename = os.path.join(image_dir, f'scene_{frame_number:05d}.jpg')
            cv2.imwrite(filename, frame)
    cap.release()


def merge_jpg_to_pdf(image_dir):
    # PDF 저장
    from PIL import Image
    from pypdf import PdfMerger, PdfReader

    # 이미지 파일 목록 가져오기
    images = [img for img in os.listdir(image_dir) if img.endswith('.jpg')]
    images.sort()

    # 이미지 파일을 PDF로 변환
    pdf_merger = PdfMerger()
    for image in images:
        im = Image.open(os.path.join(image_dir, image))

        # pdf 용량 축소를 위해 이미지 크기 변경
        resized = im.resize((int(1920/2), int(1080/2)))

        # 이미지를 바이트 스트림으로 변환한 후, PdfFileMerger에 추가
        with io.BytesIO() as byte_stream:
            resized.save(byte_stream, 'PDF')
            byte_stream.seek(0)
            pdf_merger.append(byte_stream)

    # PDF 파일 저장
    pdf_merger.write('output.pdf')
    pdf_merger.close()


if __name__ == '__main__':
    import sys

    # video url
    video_url = sys.argv[1]

    # 이미지 파일 경로 설정
    image_dir = './output'

    # 다운로드한 영상 파일 경로 설정
    video_path = 'video.mp4'

    # 씬 감지 임계값 설정
    threshold = 30

    # output 정리
    prepare_output(image_dir)

    # Video 다운로드
    download_vide(video_url)

    # 씬 감지 실행
    scene_list = detect_scenes(video_path, threshold)

    # 프레임 추출 함수 실행
    extract_frames(video_path, scene_list, image_dir)

    # PDF 저장
    merge_jpg_to_pdf(image_dir)