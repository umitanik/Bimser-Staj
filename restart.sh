#!/bin/bash

echo "Müşteri Sadakat Sistemi Yeniden Başlatılıyor..."

# Container'ları yeniden başlat
docker-compose restart

echo "Sistem yeniden başlatıldı!"
echo "Streamlit: http://localhost:8501"
echo "API: http://localhost:8000"
