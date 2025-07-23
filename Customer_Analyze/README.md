#  Müşteri Sadakat Tahmin Sistemi

Docker Compose ile çalışan modern bir müşteri sadakat tahmin sistemi.

##  Sistem Mimarisi

- **Frontend**: Streamlit (http://localhost:8501)
- **Backend**: FastAPI (http://localhost:8000) 
- **Database**: PostgreSQL (localhost:5432)
- **Container**: Docker Compose ile orkestrasyon

## 📋 Gereksinimler

###  Linux /  macOS /  Windows:
- **Docker Desktop** yüklü olmalı
- **Git** yüklü olmalı
- **Terminal/Command Prompt** erişimi

### macOS Kullanıcıları İçin:
- Docker Desktop for Mac: [İndir](https://docs.docker.com/desktop/mac/install/)
- Terminal uygulaması (varsayılan olarak yüklü)
- Homebrew ile Git: `brew install git` (isteğe bağlı)

### Windows Kullanıcıları İçin:
- Docker Desktop for Windows: [İndir](https://docs.docker.com/desktop/windows/install/)
- Git for Windows: [İndir](https://git-scm.com/download/win)
- PowerShell veya Git Bash

##  Hızlı Başlangıç

###  Projeyi İlk Kez Klonlayanlar İçin:
```bash
# 1. Projeyi klonla
git clone https://github.com/umitanik/BimserStajProje_1.git
cd BimserStajProje_1

# 2. İlk kurulum (sadece bir kez)
chmod +x setup.sh
./setup.sh

# 3. Sistemi başlat
./start.sh
```

###  Tek Komut ile Kurulum:
```bash
git clone https://github.com/umitanik/BimserStajProje_1.git && cd BimserStajProje_1 && chmod +x setup.sh && ./setup.sh && ./start.sh
```

###  Sonraki Kullanımlar:
```bash
# Sistemi başlat
./start.sh

# Sistemi durdur  
./stop.sh

# Sistemi yeniden başlat
./restart.sh
```

### 2️ Web Arayüzüne Git
[http://localhost:8501](http://localhost:8501)

### 3️ Sistemi Durdur
```bash
./stop.sh
```

##  Manuel Komutlar

### Sistemi Başlat
```bash
docker-compose up -d
```

### Durumu Kontrol Et
```bash
docker-compose ps
```

### Logları Görüntüle
```bash
docker-compose logs streamlit
docker-compose logs api
docker-compose logs postgres
```

### Sistemi Durdur
```bash
docker-compose down
```

### Tüm Verileri Sil (Dikkat!)
```bash
docker-compose down -v
```

##  Geliştirme

### Streamlit Kodunu Güncelle
1. `streamlit_app.py` dosyasını düzenle
2. Container'ı yeniden başlat:
```bash
docker-compose restart streamlit
```

### API Kodunu Güncelle
1. `api.py` dosyasını düzenle
2. Container'ı yeniden build et:
```bash
docker-compose build api
docker-compose up -d api
```

##  Sorun Giderme

### API Bağlantı Hatası
```bash
# Container durumunu kontrol et
docker-compose ps

# API loglarını kontrol et
docker-compose logs api

# API'yi test et
curl http://localhost:8000/
```

### Streamlit Hatası
```bash
# Streamlit loglarını kontrol et
docker-compose logs streamlit

# Streamlit'i yeniden başlat
docker-compose restart streamlit
```

### Veritabanı Hatası
```bash
# PostgreSQL loglarını kontrol et
docker-compose logs postgres

# Veritabanına bağlan
docker-compose exec postgres psql -U admin -d musteri_db
```

##  Container Detayları

- **musteri_postgres**: PostgreSQL 13
- **musteri_api**: FastAPI + PyTorch
- **musteri_streamlit**: Streamlit Web UI

##  API Endpoints

- `GET /` - API bilgileri
- `GET /customers` - Müşteri listesi
- `GET /stats` - İstatistikler
- `POST /predict` - Sadakat tahmini

##  Özellikler

- Gerçek zamanlı tahmin
- Veri görselleştirme  
- Müşteri analizi
- REST API entegrasyonu
- Docker ile kolay deployment
