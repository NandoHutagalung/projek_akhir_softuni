import os
import django
import schedule
import time
from django.core.management import call_command

# Inisialisasi Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projekan_akhir.settings')
django.setup()

def run_update_order_status():
    call_command('update_order_status')
    print("Perintah 'update_order_status' telah dijalankan.")

schedule.every(1).minute.do(run_update_order_status)

print("Scheduler aktif. Menunggu tugas berikutnya...")
while True:
    schedule.run_pending()
    time.sleep(1)
