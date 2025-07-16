#!/bin/bash

echo "Müşteri Sadakat Sistemi - İlk Kurulum"
echo "========================================"

# Gereksinimler kontrolü
echo "Gereksinimler kontrol ediliyor..."

# Docker kontrolü
if ! command -v docker &> /dev/null; then
    echo "Docker yüklü değil!"
    echo "Docker'ı yüklemek için: https://docs.docker.com/get-docker/"
    exit 1
fi

# Docker Compose kontrolü
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose yüklü değil!"
    echo "Docker Compose'u yüklemek için: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "Docker ve Docker Compose yüklü"

# Docker daemon kontrolü
if ! docker info &> /dev/null; then
    echo "Docker daemon çalışmıyor!"
    echo "Docker'ı başlatın: sudo systemctl start docker"
    exit 1
fi

echo "Docker daemon çalışıyor"

# Script dosyalarına izin ver
echo "Script dosyalarına çalıştırma izni veriliyor..."
chmod +x start.sh stop.sh restart.sh setup.sh

echo "İzinler ayarlandı"

# .env.example varsa .env oluştur
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    echo "Environment dosyası oluşturuluyor..."
    cp .env.example .env
    echo ".env dosyası oluşturuldu (.env.example'dan)"
fi

echo ""
echo "Kurulum tamamlandı!"
echo ""
echo "Kullanım:"
echo "  ./start.sh    - Sistemi başlat"
echo "  ./stop.sh     - Sistemi durdur"
echo "  ./restart.sh  - Sistemi yeniden başlat"
echo ""
echo "Erişim Adresleri:"
echo "Streamlit: http://localhost:8501"
echo "API:       http://localhost:8000"
echo "PostgreSQL: localhost:5432"
echo ""
echo "Şimdi sistemi başlatmak için: ./start.sh"
