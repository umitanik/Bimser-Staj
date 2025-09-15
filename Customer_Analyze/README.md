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
git clone <repository-url>
cd Customer_Analyze

# 2. Docker container'ları build et
docker-compose build

# 3. Sistemi başlat
docker-compose up -d
```

###  Tek Komut ile Kurulum:
```bash
git clone <repository-url> && cd Customer_Analyze && docker-compose build && docker-compose up -d
```

###  Sonraki Kullanımlar:
```bash
# Sistemi başlat
docker-compose up -d

# Sistemi durdur  
docker-compose down

# Sistemi yeniden başlat
docker-compose restart
```

### 2️ Web Arayüzüne Git
[http://localhost:8501](http://localhost:8501)

### 3️ Sistemi Durdur
```bash
docker-compose down
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
# Tüm servislerin logları
docker-compose logs

# Spesifik servis logları
docker-compose logs streamlit
docker-compose logs api
docker-compose logs postgres
```

### Sistemi Durdur
```bash
docker-compose down
```

### Container'ları Yeniden Build Et
```bash
docker-compose build
docker-compose up -d
```

### Tüm Verileri Sil (Dikkat!)
```bash
docker-compose down -v
docker system prune -a
```

##  Geliştirme

### Streamlit Kodunu Güncelle
1. `streamlit_app.py` dosyasını düzenle
2. Container'ı yeniden başlat:
```bash
docker-compose restart streamlit
```

### API Kodunu Güncelle
1. `API.py` dosyasını düzenle
2. Container'ı yeniden build et:
```bash
docker-compose build api
docker-compose up -d api
```

### Model Güncelleme
1. `complete_model.pkl` dosyasını güncelle
2. API container'ını yeniden başlat:
```bash
docker-compose restart api
```

##  Sorun Giderme

### Portlar Kullanımda Hatası
```bash
# Kullanılan portları kontrol et
lsof -i :8501  # Streamlit portu
lsof -i :8000  # FastAPI portu
lsof -i :5432  # PostgreSQL portu

# Çakışan servisleri durdur
sudo kill -9 <PID>
```

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

# Browser cache'ini temizle
```

### Veritabanı Hatası
```bash
# PostgreSQL loglarını kontrol et
docker-compose logs postgres

# Veritabanına bağlan (eğer varsa)
docker-compose exec postgres psql -U admin -d musteri_db

# Volume'ları temizle
docker-compose down -v
```

### Docker Build Hatası
```bash
# Cache'siz build
docker-compose build --no-cache

# Docker system temizle
docker system prune -a

# Yeniden build ve başlat
docker-compose build && docker-compose up -d
```

##  Container Detayları

- **streamlit**: Streamlit Web UI (Port: 8501)
- **api**: FastAPI Backend (Port: 8000)  
- **postgres**: PostgreSQL Database (Port: 5432) - eğer kullanılıyorsa

##  API Endpoints

- `GET /` - API bilgileri
- `GET /customers` - Müşteri listesi  
- `GET /stats` - İstatistikler
- `POST /predict` - Sadakat tahmini

##  Özellikler

- ✅ Gerçek zamanlı tahmin
- ✅ Veri görselleştirme  
- ✅ Müşteri analizi
- ✅ REST API entegrasyonu
- ✅ Docker ile kolay deployment
- ✅ Machine Learning model entegrasyonu

##  Dosya Yapısı

```
Customer_Analyze/
├── API.py                 # FastAPI backend
├── streamlit_app.py       # Streamlit frontend
├── data_processing.py     # Veri işleme
├── database.py           # Veritabanı işlemleri
├── complete_model.pkl    # Eğitilmiş ML modeli
├── docker-compose.yml    # Container orkestrasyon
├── Dockerfile           # API container tanımı
├── Dockerfile.streamlit # Streamlit container tanımı
├── requirements.txt     # Python bağımlılıkları
└── README.md           # Bu dosya
```

##  İletişim

Sorunlar için issue açabilir veya geliştirici ile iletişime geçebilirsiniz.
