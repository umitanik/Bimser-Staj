#!/bin/bash

echo "🔄 Müşteri Sadakat Sistemi Başlatılıyor..."

# Önceki container'ları temizle
echo "🧹 Önceki container'ları temizleniyor..."
docker-compose down

# Sistemi başlat
echo "🚀 Sistem başlatılıyor..."
docker-compose up -d

# Container'ların hazır olmasını bekle
echo "⏳ Container'lar hazırlanıyor..."
sleep 10

# Sağlık kontrolü
echo "🔍 Sistem durumu kontrol ediliyor..."
docker-compose ps

echo "✅ Sistem hazır!"
echo "📊 Streamlit: http://localhost:8501"
echo "🔗 API: http://localhost:8000"
echo "🗄️  PostgreSQL: localhost:5432"

# API test et
echo "🧪 API testi yapılıyor..."
docker-compose exec -T streamlit python -c "
import requests
import os
try:
    response = requests.get('http://api:8000/')
    if response.status_code == 200:
        print('✅ API çalışıyor!')
    else:
        print('❌ API hatası:', response.status_code)
except Exception as e:
    print('❌ Bağlantı hatası:', e)
"
