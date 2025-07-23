# 🔍 Embedding Modelleri Benzerlik Analizi Raporu

Bu rapor, 8 farklı embedding modelinin **Türkçe-İngilizce kurumsal terimler** üzerindeki performansını karşılaştıran kapsamlı bir analiz sunmaktadır.

## 📋 Proje Özeti

Bu proje, farklı embedding modellerinin **cosine similarity** kullanarak Türkçe ve İngilizce kurumsal terimler arasındaki anlamsal benzerliği ne kadar iyi yakaladığını ölçmektedir. Test sistemi özellikle **Türkçe-İngilizce çeviri doğruluğuna** odaklanmaktadır.

### Temel Amaçlar:
- ✅ 8 farklı embedding modelinin karşılaştırılması  
- ✅ Kurumsal terminoloji için en uygun modelin belirlenmesi
- ✅ **Türkçe-İngilizce çeviri kalitesinin öncelikli değerlendirilmesi**
- ✅ Model performanslarının kategorik analizi
- ✅ **Mantıklı değerlendirme kriterleri** (sadece çeviri testleri sayılır)

---

## 🤖 Test Edilen Modeller

| Model Adı | Tür | Özellikler | Model Boyutu | Öne Çıkan Özellik |
|-----------|-----|------------|--------------|-------------------|
| **Alibaba GTE** | Sentence Transformer | Çok dilli, genel amaçlı | ~560MB | Güçlü çok dilli destek |
| **E5 Multilingual** | Transformer | Microsoft, çok dilli | ~1.1GB | Akademik/profesyonel |
| **E5 Small** | Transformer | Hafif versiyon | ~470MB | Hız ve verimlilik |
| **DistilUSE v1** | Sentence Transformer | Distilled model | ~510MB | Hızlı işlem |
| **Nomic AI** | Transformer | Mixture of Experts | ~1.4GB | Karmaşık analiz |
| **LaBSE** | Sentence Transformer | Google, dil agnostik | ~470MB | 109 dil desteği |
| **Trendyol** | Sentence Transformer | E-ticaret, Türkçe odaklı | ~470MB | **Türkçe optimize** |
| **Snowflake Arctic** | Sentence Transformer | Yeni nesil, prompt destekli | ~560MB | Modern mimari |

### 🎯 Önemli Not:
Sistem, model performansını değerlendirirken **sadece Türkçe-İngilizce çeviri testlerini (ilk 24 test)** dikkate alır. Zıt anlamlar ve ilgisiz kelimeler sadece model davranışını anlamak için kullanılır.

---

## 🔬 Test Metodolojisi

### Değerlendirme Sistemi:
- **Ana Metrik**: Sadece **Türkçe-İngilizce çeviri testleri** (24/60 test) değerlendirmeye dahil
- **Kazanan Belirleme**: Her testte en yüksek cosine similarity skorunu alan model 1 puan alır
- **Final Sıralama**: X/24 test kazanan model formatında gösterilir
- **Kategorik Analiz**: Tüm kategorilerde ortalama performans ayrıca hesaplanır

### Benzerlik Hesaplama:
- **Cosine Similarity** algoritması kullanılmıştır
- Her kelime çifti için embedding vektörleri oluşturulur
- Vektörler arasındaki açının kosinüsü hesaplanır (-1 ile +1 arası)
- Pozitif değerler benzerlik, negatif değerler farklılık gösterir

### Test Kategorileri:

#### 1. 🎯 **Türkçe-İngilizce Çeviriler** (SIRALAMADA ETKİLİ)
**Bu testler model sıralamasını belirler - Yüksek benzerlik beklenir (>0.8)**
- mali rapor ↔ financial report
- vergi ↔ tax  
- fatura ↔ invoice
- sözleşme ↔ contract
- şirket ↔ company
- yönetim kurulu ↔ board of directors
- hisse ↔ stock
- bilanço ↔ balance sheet
- muhasebe ↔ accounting
- bütçe ↔ budget
- nakit akışı ↔ cash flow
- karlılık ↔ profitability
- satış ↔ sales
- pazarlama ↔ marketing
- insan kaynakları ↔ human resources
- işe alım ↔ recruitment
- maaş bordrosu ↔ payroll
- performans değerlendirmesi ↔ performance evaluation
- operasyon ↔ operation
- proje yönetimi ↔ project management
- risk analizi ↔ risk analysis
- iş planı ↔ business plan
- strateji ↔ strategy
- yatırım ↔ investment

#### 2. 📊 **Benzer Anlamlar** (Sadece analiz için)
Yakın anlamlı Türkçe terimler - Orta benzerlik beklenir (0.5-0.7):
- fatura ↔ ödeme belgesi
- hisse ↔ pay
- yönetici ↔ müdür  
- gider ↔ harcama
- karlılık ↔ getiri
- personel ↔ çalışan
- müşteri ↔ istemci
- satış ↔ ticaret
- toplantı ↔ görüşme
- rapor ↔ doküman
- analiz ↔ inceleme
- planlama ↔ organizasyon

#### 3. 🔄 **Zıt Anlamlar** (Sadece analiz için)
Karşıt anlamlı finansal terimler - Düşük benzerlik beklenir (<0.3):
- gelir ↔ gider
- kâr ↔ zarar
- aktif ↔ pasif
- alacak ↔ borç
- satış ↔ satın alma
- artış ↔ azalış
- başarı ↔ başarısızlık
- verimlilik ↔ verimsizlik
- genişleme ↔ küçülme
- yatırım ↔ geri çekme
- yükselme ↔ düşüş
- kazanç ↔ kayıp

#### 4. ❌ **İlgisiz Kelimeler** (Sadece analiz için)
Hiçbir anlam ilişkisi olmayan terimler - Çok düşük benzerlik (<0.2):
- bilanço ↔ çalışan motivasyonu
- vergi ↔ şirket logosu
- sözleşme ↔ müzik listesi
- yönetim kurulu ↔ hava durumu raporu
- muhasebe ↔ spor müsabakası
- mali rapor ↔ yemek tarifi
- nakit akışı ↔ film eleştirisi
- karlılık ↔ bahçe tasarımı
- proje yönetimi ↔ moda trendi
- risk analizi ↔ seyahat rehberi
- performans değerlendirmesi ↔ müze koleksiyonu
- insan kaynakları ↔ uzay araştırması

---

## ⚙️ Kurulum ve Çalıştırma Talimatları

### Gerekli Kütüphaneler:
```bash
pip install sentence-transformers
pip install transformers  
pip install torch
pip install einops  # Kritik bağımlılık!
```

### Test Çalıştırma:
```bash
cd LLM_Cosine_Similarity
python Models_Test.py
```

### Test Sürecinin Aşamaları:
1. **Model Yükleme**: 8 model RAM'e yüklenir (~3-6 dakika, ~8GB RAM gerekli)
2. **Test Başlatma**: 60 kelime çifti sırayla test edilir  
3. **Benzerlik Hesaplama**: Her model için cosine similarity hesaplanır
4. **Sıralama**: Sadece Türkçe-İngilizce çeviri testleri değerlendirilir
5. **Rapor Oluşturma**: Kategorik analiz ve model sıralaması gösterilir

### Çıktı Formatı:
```
🔧 Modeller yükleniyor...
Bu işlem biraz zaman alabilir...

KAPSAMLI MODEL TEST SİSTEMİ
================================================================================

 Test  1/60: 'mali rapor' ↔ 'financial report'  
------------------------------------------------------------
     Alibaba GTE: 0.8543
  E5 Multilingual: 0.8721  
         E5 Small: 0.8432
     DistilUSE v1: 0.7865
         Nomic AI: 0.8234
           LaBSE: 0.8876
        Trendyol: 0.8654
 Snowflake Arctic: 0.8798

[...diğer testler...]

================================================================================
📊 GENEL SONUÇLAR VE ANALİZ
================================================================================

🏆 MODEL ORTALAMA PERFORMANSLARI:
--------------------------------------------------

🥊 TÜRKÇE-İNGİLİZCE ÇEVİRİ BAŞARI SONUÇLARI:
---------------------------------------------
  1. LaBSE: 18/24 test kazandı
  2. Snowflake Arctic: 4/24 test kazandı  
  3. Trendyol: 2/24 test kazandı
  [...]
```

### 🎯 İdeal Model Özellikleri:
✅ **Türkçe-İngilizce çevirilerde yüksek skor** (>0.80) - Ana kriter  
✅ **Zıt anlamlarda düşük skor** (<0.30) - Model güvenilirliği  
✅ **İlgisiz kelimelerde çok düşük skor** (<0.20) - Yanlış pozitif önleme  
✅ **Benzer anlamlarda orta düzey skor** (0.50-0.70) - Anlam ayrımı  
✅ **Tutarlı performans** - Kategoriler arası dengeli davranış

### ⚠️ Değerlendirme Kriterleri:
- **Model sıralaması**: Sadece Türkçe-İngilizce çeviri testlerinde kazanılan test sayısına göre
- **Kategorik analiz**: Tüm testlerin ortalaması (model davranışını anlamak için)
- **Başarı ölçütü**: X/24 test kazandı formatında gösterilir  

---

## 🔧 Teknik Detaylar

### Model Mimarileri ve Boyutları:
| Model | Mimari | Embedding Boyutu | Tokenizasyon | Özel Özellik |
|-------|--------|------------------|--------------|--------------|
| Alibaba GTE | BERT-like | 768 | WordPiece | Çok dilli optimize |
| E5 Multilingual | BERT-like | 768 | WordPiece | "query: " prefix |
| E5 Small | BERT-like | 384 | WordPiece | "query: " prefix |
| DistilUSE | DistilBERT | 512 | WordPiece | Sıkıştırılmış |
| Nomic AI | MoE | 768 | Custom | Mixture of Experts |
| LaBSE | BERT-like | 768 | SentencePiece | 109 dil desteği |
| Trendyol | BERT-like | 768 | WordPiece | E-ticaret odaklı |
| Snowflake Arctic | BERT-like | 1024 | WordPiece | Prompt desteği |

### Özel Test Fonksiyonları:

#### Sentence Transformer Modelleri:
```python
def test_sentence_transformer_model(model, word1, word2):
    emb1 = model.encode(word1, convert_to_tensor=True)
    emb2 = model.encode(word2, convert_to_tensor=True)
    return util.pytorch_cos_sim(emb1, emb2).item()
```

#### Snowflake Arctic (Prompt Destekli):
```python
def test_snowflake_model(model, word1, word2):
    query_emb = model.encode([word1], prompt_name="query", convert_to_tensor=True)
    doc_emb = model.encode([word2], convert_to_tensor=True)
    return util.pytorch_cos_sim(query_emb, doc_emb).item()
```

#### Transformer Modelleri (E5, Nomic AI):
```python
def test_transformers_model(model, tokenizer, word1, word2, prefix=""):
    texts = [f"{prefix}{word1}", f"{prefix}{word2}"]
    batch = tokenizer(texts, max_length=512, padding=True, 
                     truncation=True, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model(**batch)
    
    embeddings = average_pool(outputs.last_hidden_state, batch['attention_mask'])
    embeddings = F.normalize(embeddings, p=2, dim=1)
    
    return (embeddings[0] @ embeddings[1].T).item()
```

#### Average Pooling Fonksiyonu:
```python
def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
```

---

## 📊 Sonuç Analizi ve Yorumlama

Bu bölümde, test sonuçlarının nasıl değerlendirileceği ve modellerin farklı kullanım senaryolarına göre nasıl seçileceği açıklanmaktadır.

### 📈 Rapor Çıktıları:

#### 1. 🏆 **Model Ortalama Performansları**
- **Kapsam**: Tüm 60 testin genel ortalaması
- **Amaç**: Modellerin genel benzerlik yakalaması yeteneğini gösterir
- **Not**: Bu ortalama **sıralama için kullanılmaz** (zıt anlamlar skorları yükseltebilir)

#### 2. 📈 **Kategori Analizi**
- **Türkçe-İngilizce Çeviriler**: En önemli kategori, yüksek skor beklenir
- **Benzer Anlamlar**: Model nüansları yakalama yeteneği
- **Zıt Anlamlar**: Modelin karışmasını engelleyebilme
- **İlgisiz Kelimeler**: Yanlış pozitif önleme kabiliyeti

#### 3. 🥊 **Türkçe-İngilizce Çeviri Başarı Sonuçları** 
- **Ana Metrik**: Model sıralaması sadece buna dayanır
- **Format**: "X/24 test kazandı" şeklinde gösterilir
- **Mantık**: Her testte en yüksek benzerlik skoru alan model 1 puan kazanır

#### 4. 🎯 **En Yüksek/Düşük Skorlar**
- Dikkat çeken anormal sonuçların belirlenmesi
- Model davranışlarının detaylı analizi

### 🎯 Model Seçim Kriterleri:

#### 🏆 **Genel Amaçlı Kullanım:**
- **LaBSE**: 
  - ✅ 109 dil desteği, Google'ın çok dilli modeli
  - ✅ Dengeli performans, güvenilir sonuçlar
  - ✅ Kurumsal projeler için ideal
- **Alibaba GTE**: 
  - ✅ Çok dilli desteği güçlü
  - ✅ Orta boyutlu, makul kaynak kullanımı
  - ✅ Genel amaçlı projeler için uygun
- **Snowflake Arctic**: 
  - ✅ En yeni nesil embedding modeli
  - ✅ Prompt destekli özellikler
  - ✅ Modern AI uygulamaları için optimize

#### 🇹🇷 **Türkçe Odaklı Projeler:**
- **Trendyol**: 
  - ✅ Türkçe e-ticaret verisi ile eğitilmiş
  - ✅ Türkçe kurumsal terimler için optimize
  - ✅ Yerel şirketlerin projelerine uygun
- **LaBSE**: 
  - ✅ Türkçe dahil 109 dil desteği
  - ✅ Çok dilli projeler için ideal
  - ✅ Google'ın dil agnostik yaklaşımı

#### ⚡ **Performans Odaklı:**
- **E5 Small**: 
  - ✅ En hafif model (~470MB)
  - ✅ Hızlı işlem, düşük kaynak tüketimi
  - ✅ Mobil uygulamalar için uygun
- **DistilUSE v1**: 
  - ✅ Distilled (sıkıştırılmış) mimari
  - ✅ İyi performans/boyut oranı
  - ✅ Edge computing için optimize

#### 🔬 **Araştırma ve Geliştirme:**
- **Nomic AI**: 
  - ✅ Mixture of Experts mimarisi
  - ✅ Karmaşık anlamsal analizler için güçlü
  - ✅ Deneysel projeler ve araştırmalar için
- **E5 Multilingual**: 
  - ✅ Microsoft'un akademik standardı
  - ✅ Peer-reviewed araştırmalarda kullanılır
  - ✅ Bilimsel çalışmalar için referans model

### ⚠️ Önemli Değerlendirme Notları:

#### 🎯 **Sıralama Mantığı:**
- **✅ Doğru**: Sadece Türkçe-İngilizce çeviri testleri sayılır
- **❌ Yanlış**: Tüm testlerin ortalamasına bakmak
- **Sebep**: Zıt anlamlar ve ilgisiz kelimeler farklı amaçlara hizmet eder

#### 📊 **Kategorik Analiz Amacı:**
- Model davranışını **anlamak** için kullanılır
- Sıralama için **kullanılmaz**
- Hangi durumda hangi modelin güçlü/zayıf olduğunu gösterir

#### 🔍 **Yüksek Ortalama Tuzağı:**
- Yüksek genel ortalama ≠ İyi çeviri performansı
- Zıt anlamlar kategorisinde yüksek skor kötü bir işaret olabilir
- İlgisiz kelimeler kategorisinde yüksek skor problem gösterir

#### 🏅 **Mükemmel Performans:**
- **24/24 test kazanan model** mutlaka en iyidir
- Böyle bir model tüm çeviri testlerinde birinci gelmiştir
- Gerçek projeler için en güvenilir seçimdir

---

## 🎯 Proje Sonucu ve Değerlendirme

Bu analiz sistemi, **Türkçe-İngilizce kurumsal terminoloji** için en uygun embedding modelini bilimsel yöntemlerle belirlemeyi amaçlamaktadır.

### ✅ Başarılan Hedefler:
- 8 farklı embedding modelinin kapsamlı karşılaştırılması
- Mantıklı değerlendirme kriterlerinin geliştirilmesi  
- Kategorik analiz ile model davranışlarının anlaşılması
- Türkçe-İngilizce çeviri odaklı sıralama sistemi
- Teknik detayları içeren kapsamlı dokümantasyon
- 60 test verisi ile genişletilmiş kapsamlı analiz

### 🔮 Gelecek Geliştirmeler:
- Daha fazla kurumsal terminoloji eklenmesi
- Domain-specific model fine-tuning
- Çoklu metrik değerlendirme (BLEU, ROUGE vb.)
- Batch processing optimizasyonları  
- Web arayüzü geliştirilmesi
- Sektörel özelleştirmeler (finans, teknoloji, sağlık vb.)

### 📈 Beklenen Sonuçlar:
Test tamamlandıktan sonra aşağıdaki formatda sonuçlar elde edilecek:

```
🥊 TÜRKÇE-İNGİLİZCE ÇEVİRİ BAŞARI SONUÇLARI:
---------------------------------------------
  1. [Model Adı]: X/24 test kazandı
  2. [Model Adı]: Y/24 test kazandı
  3. [Model Adı]: Z/24 test kazandı
  ...
```

### 🚀 Kullanım Önerileri:
- **Proje başlangıcında**: Model seçimi için test çalıştırın
- **Performans analizi**: Kategorik sonuçları inceleyin  
- **Optimizasyon**: Sadece çeviri testlerindeki başarıya odaklanın
- **Model değiştirme**: Yeni modeller ekleyerek karşılaştırın
- **A/B Testing**: Farklı modelleri gerçek verilerle karşılaştırın

---

## 📞 Destek ve İletişim

**📅 Rapor Tarihi**: Temmuz 2025  
**🔬 Test Versiyonu**: v2.1 (Cleaned & Optimized)  
**👨‍💻 Geliştirici**: Ümit Anık  
**🏢 Proje**: BimserStajProje_1  
**⚡ Son Güncelleme**: Rapor tamamen yeniden düzenlendi

### 📁 Dosya Yapısı:
```
LLM_Cosine_Similarity/
├── Models_Test.py          # Ana test sistemi (60 test)
├── SIMILARITY_REPORT.md    # Bu rapor
└── [Test sonuçları]        # Otomatik oluşturulacak
```

### 🖥️ Sistem Gereksinimleri:
- **Python**: 3.8+
- **RAM**: ~8GB (model yükleme için)
- **Disk**: ~10GB (model indirme için)
- **GPU**: CUDA destekli GPU (önerilen, opsiyonel)
- **İnternet**: Model indirme için gerekli

### ⚡ Hızlı Başlangıç:
```bash
# Klasöre geçiş
cd LLM_Cosine_Similarity

# Bağımlılıkları yükle
pip install sentence-transformers transformers torch einops

# Testi çalıştır
python Models_Test.py
```

### 🔧 Sorun Giderme:
- **ModuleNotFoundError**: `pip install` komutlarını tekrar çalıştırın
- **CUDA Error**: CPU modunda çalıştırmayı deneyin
- **Memory Error**: Daha az model ile test edin
- **Network Error**: İnternet bağlantınızı kontrol edin
