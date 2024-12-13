from django.http import StreamingHttpResponse
import time
import json
from pesanan.models import Pesanan
from meja_biliar.models import MejaBiliar
from datetime import datetime, timedelta
from django.db.models import F, ExpressionWrapper, fields
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.utils import timezone

# Fungsi untuk memeriksa pesanan baru yang belum dikirim
def cek_pesanan_baru():
    while True:
        # Menyaring pesanan yang belum dikirim (is_send = 0)
        pesanan_baru = Pesanan.objects.filter(is_send=0)
        if pesanan_baru.exists():
            for pesanan in pesanan_baru:
                # Mendapatkan nomor meja dari tabel MejaBiliar berdasarkan ID
                no_meja = MejaBiliar.objects.get(id=pesanan.meja_id).no_meja
                # Mengirim data ke klien melalui EventStream
                yield f"data: \"Pesanan baru untuk meja nomor: {no_meja}\"\n\n"
            # Memperbarui status is_send menjadi 1 untuk menandai bahwa pesanan telah dikirim
            pesanan_baru.update(is_send=1)
        else:
            # Jika tidak ada pesanan baru, tunggu beberapa waktu sebelum memeriksa ulang
            time.sleep(1)

def cek_pesanan_hampir_selesai():
    pesanan_selesai = Pesanan.objects.filter(
        waktu_notif__lte=timezone.now(), 
        notifikasi_dikirim=False
    )

    if pesanan_selesai.exists():
        print("Pesanan yang memenuhi kondisi ditemukan")
        for pesanan in pesanan_selesai:
            no_meja = MejaBiliar.objects.get(id=pesanan.meja_id).no_meja
            waktu_notifikasi = pesanan.waktu_notif.strftime('%Y-%m-%d %H:%M:%S')  # Format waktu_notifikasi
            print(f"Notifikasi: [{waktu_notifikasi}] Pesanan untuk meja nomor {no_meja} hampir selesai.")
            yield f"data: \"Pesanan untuk meja nomor {no_meja} hampir selesai.\"\n\n"
            pesanan.notifikasi_dikirim = True  
            pesanan.save()
    else:
        time.sleep(1)


def event_streamm():
    while True:
        yield from cek_pesanan_baru()
        time.sleep(1)
def event_stream():
    while True:
        yield from cek_pesanan_hampir_selesai()
        time.sleep(1)

def sse_notifikasi(request):
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

def sse_notifikasii(request):
    response = StreamingHttpResponse(event_streamm(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
