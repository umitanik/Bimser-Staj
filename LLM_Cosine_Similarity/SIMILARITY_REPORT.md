# 🔍 Embedding Modelleri Benzerlik Analizi Raporu

Bu rapor, 8 farklı embedding modelinin **Türkçe-İngilizce kurumsal terimler** üzerindeki performansını karşılaştıran kapsamlı bir analiz sunmaktadır.

##  Proje Özeti

Bu proje, farklı embedding modellerinin **cosine similarity** kullanarak Türkçe ve İngilizce kurumsal terimler arasındaki anlamsal benzerliği ne kadar iyi yakaladığını ölçmektedir.

### Temel Amaçlar:
- ✅ Çok dilli embedding modellerinin karşılaştırılması
- ✅ Kurumsal terminoloji için en uygun modelin belirlenmesi
- ✅ Türkçe-İngilizce çeviri kalitesinin değerlendirilmesi
- ✅ Model performanslarının kategorik analizi

---

##  Test Edilen Modeller

| Model Adı | Tür | Özellikler | Kullanım Alanı |
|-----------|-----|------------|-----------------|
| **Alibaba GTE** | Sentence Transformer | Çok dilli, genel amaçlı | Genel benzerlik analizi |
| **E5 Multilingual** | Transformer | Microsoft, çok dilli | Akademik/profesyonel |
| **E5 Small** | Transformer | Hafif versiyon | Hızlı işlem gerekli durumlar |
| **DistilUSE v1** | Sentence Transformer | Distilled model | Performans odaklı |
| **Nomic AI** | Transformer | Mixture of Experts | Karmaşık analiz |
| **LaBSE** | Sentence Transformer | Google, dil agnostik | Çok dilli uygulamalar |
| **Trendyol** | Sentence Transformer | E-ticaret odaklı, Türkçe | Türkçe metinler |
| **Snowflake Arctic** | Sentence Transformer | Yeni nesil, prompt destekli | Modern uygulamalar |

---

##  Test Metodolojisi

### Benzerlik Hesaplama:
- **Cosine Similarity** algoritması kullanılmıştır
- Her kelime çifti için embedding vektörleri oluşturulur
- Vektörler arasındaki açının kosinüsü hesaplanır
- Sonuçlar 0-1 arasında normalize edilir

### Test Kategorileri:

#### 1.  Türkçe-İngilizce Çeviriler (Yüksek Benzerlik Beklenir)
Aynı anlamı taşıyan Türkçe ve İngilizce kurumsal terimler:
- mali rapor ↔ financial report
- vergi ↔ tax
- fatura ↔ invoice
- sözleşme ↔ contract
- şirket ↔ company
- yönetim kurulu ↔ board of directors
- hisse ↔ stock
- bilanço ↔ balance sheet

#### 2.  Benzer Anlamlar (Orta Benzerlik Beklenir)
Yakın anlamlı Türkçe terimler:
- fatura ↔ ödeme belgesi
- hisse ↔ pay
- yönetici ↔ müdür
- gider ↔ harcama

#### 3.  Zıt Anlamlar (Düşük Benzerlik Beklenir)
Karşıt anlamlı finansal terimler:
- gelir ↔ gider
- kâr ↔ zarar
- aktif ↔ pasif
- alacak ↔ borç

#### 4.  İlgisiz Kelimeler (Çok Düşük Benzerlik Beklenir)
Hiçbir anlam ilişkisi olmayan terimler:
- bilanço ↔ çalışan motivasyonu
- vergi ↔ şirket logosu
- sözleşme ↔ müzik listesi
- yönetim kurulu ↔ hava durumu raporu

---

##  Kurulum Talimatları

### Gerekli Kütüphaneler:
```bash
pip install sentence-transformers
pip install transformers
pip install torch
pip install numpy
```

### Test Sürecinin Aşamaları:
1. **Model Yükleme**: Tüm modeller RAM'e yüklenir (~2-5 dakika)
2. **Test Başlatma**: 20 kelime çifti test edilir
3. **Benzerlik Hesaplama**: Her model için cosine similarity hesaplanır
4. **Rapor Oluşturma**: Sonuçlar kategorize edilir ve analiz edilir

### Çıktı Formatı:
```
🚀 KAPSAMLI MODEL TEST SİSTEMİ
================================================================================

📍 Test 1/20: 'mali rapor' ↔ 'financial report'
------------------------------------------------------------
     Alibaba GTE: 0.8543
  E5 Multilingual: 0.8721
         E5 Small: 0.8432
     DistilUSE v1: 0.7865
         Nomic AI: 0.8234
           LaBSE: 0.8876
        Trendyol: 0.8654
 Snowflake Arctic: 0.8798
```

### İdeal Model Özellikleri:
✅ Türkçe-İngilizce çevirilerde yüksek skor (>0.8)  
✅ Zıt anlamlarda düşük skor (<0.3)  
✅ İlgisiz kelimelerde çok düşük skor (<0.2)  
✅ Benzer anlamlarda orta düzey skor (0.5-0.7)  

---

## 🔧 Teknik Detaylar

### Embedding Boyutları:
- Çoğu model: 384-768 boyut
- Büyük modeller: 1024+ boyut

### Tokenizasyon:
- **BERT-based**: WordPiece tokenization
- **Sentence Transformers**: Otomatik preprocessing
- **E5 modelleri**: Özel prefix ("query: ")

### Özel Fonksiyonlar:

#### Snowflake Arctic için:
```python
def test_snowflake_model(model, word1, word2):
    query_emb = model.encode([word1], prompt_name="query")
    doc_emb = model.encode([word2])
    return cosine_similarity(query_emb, doc_emb)
```

#### Transformer modelleri için:
```python
def test_transformers_model(model, tokenizer, word1, word2, prefix=""):
    texts = [f"{prefix}{word1}", f"{prefix}{word2}"]
    # Encoding ve similarity hesaplama
```

---

## 📋 Sonuç Analizi

### Raporda Yer Alacak Bilgiler:
- **Model Sıralaması**: En başarılıdan en düşük performanslıya
- **Kategori Analizi**: Her kategoride hangi model en iyi
- **En Yüksek/Düşük Skorlar**: Dikkat çeken sonuçlar
- **Öneri ve Tavsiyeleri**: Hangi model hangi durumda kullanılmalı

### Kullanım Tavsiyeleri:
- **Genel Amaçlı**: LaBSE veya Alibaba GTE
- **Türkçe Odaklı**: Trendyol modeli
- **Hız Odaklı**: E5 Small
- **Modern Özellikler**: Snowflake Arctic

---

## 🎯 Sonuç

Bu analiz, kurumsal Türkçe-İngilizce terminoloji için en uygun embedding modelini seçmek amacıyla tasarlanmıştır. Sonuçlar, proje gereksinimlerinize göre model seçimi yapmanızda rehberlik edecektir.

### Test Tamamlandıktan Sonra:
- Detaylı performans tabloları
- Model önerileri
- Kullanım senaryoları
- Optimizasyon tavsiyeleri

---

**📅 Rapor Tarihi**: Ocak 2025  
**🔬 Test Versiyonu**: v1.0  
**⚡ Güncelleme**: Test sonrası otomatik güncellenecek
