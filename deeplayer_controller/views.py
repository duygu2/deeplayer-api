

'''
def generate_animation(request):
    # Gelen isteği kontrol etme
    if 'photo' not in request.FILES or 'video' not in request.FILES:
        return JsonResponse({'error': 'Photo or video not found.'}, status=400)
    
    photo = request.FILES['photo']
    video = request.FILES['video']

    # Fotoğraf ve videoyu geçici dosyalara kaydetme
    photo_path = 'first_order_model/source_image/photo.png'
    video_path = 'first_order_model/driving_video/video.mp4'
    with open(photo_path, 'wb') as f:
        for chunk in photo.chunks():
            f.write(chunk)
    with open(video_path, 'wb') as f:
        for chunk in video.chunks():
            f.write(chunk)

    # Animasyon oluşturma için gerekli dosya yolları
    config_path = 'first_order_model/config/vox-adv-256.yaml'
    checkpoint_path = 'first_order_model/fom_checkpoint/vox-adv-cpk.pth.tar'
    result_path = 'first_order_model/result.mp4'
    print("29 çalışıyor")
    try:
        # Modeli yükleme
        generator, kp_detector = load_checkpoints(config_path, checkpoint_path)

        # Kaynak görüntü ve sürüş videosundan animasyon oluşturma
        # Kaynak görüntü ve sürüş videosundan animasyon oluşturma
        predictions = make_animation(photo_path, video_path, generator, kp_detector, relative=True, adapt_movement_scale=True)


        # Tahminleri birleştirerek animasyonu oluşturma
        imageio.mimsave(result_path, [img_as_ubyte(frame) for frame in predictions], fps=30)

        # Oluşturulan animasyonun sonucunu döndürme
        with open(result_path, 'rb') as f:
            result_data = f.read()
        return JsonResponse({'result': result_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': repr(e)}, status=500)

'''


from django.shortcuts import render
from django.http import JsonResponse

from django.http import JsonResponse
import json
import os
import subprocess
import PIL.Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from django.shortcuts import render
from django.http import JsonResponse

import shutil

import os
import imageio
import shutil

import subprocess
import os
import subprocess
from django.http import JsonResponse

class VideoProcessor:
    def __init__(self):
        self.output_dir = os.path.abspath('first_order_model/output')

    def process_video(self, config_file, driving_video, source_image, checkpoint):
        # Videoyu işleme
        result_video = os.path.join(self.output_dir, 'outputt.mp4')
        command = f'python C:/Users/Duygu/Desktop/deeplayer-api/deeplayer_api/first_order_model/demo.py --config {config_file} --driving_video {driving_video} --source_image {source_image} --checkpoint {checkpoint} --relative --adapt_scale --result_video {result_video}'

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print("Hata oluştu:", stderr.decode())
            return None

        # İşlem sonucunu döndürme
        return result_video

def hello(request):
    return JsonResponse({"message": "Hello"})

def generate_animation(request):
    # Gelen isteği kontrol etme
    if 'photo' not in request.FILES or 'video' not in request.FILES:
        return JsonResponse({'error': 'Photo or video not found.'}, status=400)

    photo_file = request.FILES['photo']
    video_file = request.FILES['video']

    # Gerekli dosya yollarını ve konfigürasyon dosyasını ayarlama
    model_dir = 'first_order_model'
    config_file = os.path.join(model_dir, 'config', 'vox-adv-256.yaml')
    driving_video_path = os.path.join(model_dir, 'driving_video', 'videooo.mp4')
    source_image_path = os.path.join(model_dir, 'source_image', 'photooo.png')
    checkpoint_path = os.path.join(model_dir, 'fom_checkpoint', 'vox-adv-cpk.pth.tar')

    # Dosyaları geçici olarak kaydetme
    with open(driving_video_path, 'wb') as f:
        for chunk in video_file.chunks():
            f.write(chunk)

    with open(source_image_path, 'wb') as f:
        for chunk in photo_file.chunks():
            f.write(chunk)

    # Video işleme işlemlerini gerçekleştiren sınıfın örneğini oluşturma
    video_processor = VideoProcessor()
    print("helloo")
    # Videoyu işleme
    result_path = video_processor.process_video(config_file, driving_video_path, source_image_path, checkpoint_path)

    # Dosya kaydetme dizinini belirleme
    os.makedirs(video_processor.output_dir, exist_ok=True)

    if result_path is None:
        # Hata durumunda uygun bir yanıt döndürme
        return JsonResponse({'error': 'Video processing failed.'}, status=500)

    # Oluşturulan animasyonun sonucunu döndürme
    if os.path.exists(result_path):
        print("Dosya bulundu:", result_path)
    else:
        print("Dosya bulunamadı:", result_path)

    return JsonResponse({'result': result_path})
"""
    # Animation paths
    config_path = 'first_order_model/config/vox-adv-256.yaml'
    checkpoint_path = 'first_order_model/fom_checkpoint/vox-adv-cpk.pth.tar'
    result_path = 'first_order_model/result.mp4'
"""