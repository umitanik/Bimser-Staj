#!/bin/bash

echo "🛑 Müşteri Sadakat Sistemi Durduruluyor..."

# Tüm container'ları durdur
docker-compose down

echo "✅ Sistem durduruldu!"
echo "💾 Veriler korundu (PostgreSQL volume)"
