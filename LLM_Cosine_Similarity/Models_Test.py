from sentence_transformers import SentenceTransformer, util
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import warnings
import torch
warnings.filterwarnings('ignore')


models = {
    "alibaba": {
        "model": SentenceTransformer('Alibaba-NLP/gte-multilingual-base', trust_remote_code=True),
        "type": "sentence"
    },

    "e5": {
        "model": AutoModel.from_pretrained('intfloat/multilingual-e5-base'),
        "tokenizer": AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base'),
        "prefix": "query: ",
        "type": "transformer"
    },

    "e5_small": {
        "model": AutoModel.from_pretrained('intfloat/multilingual-e5-small'),
        "tokenizer": AutoTokenizer.from_pretrained('intfloat/multilingual-e5-small'),
        "prefix": "query: ",
        "type": "transformer"
    },

    "distiluse_v1": {
        "model": SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1'),
        "type": "sentence"
    },

    "nomic_ai": {
        "model": AutoModel.from_pretrained("nomic-ai/nomic-embed-text-v2-moe", trust_remote_code=True),
        "tokenizer": AutoTokenizer.from_pretrained("nomic-ai/nomic-embed-text-v2-moe"),
        "type": "transformer"
    },

    "labse": {
        "model": SentenceTransformer('sentence-transformers/LaBSE'),
        "type": "sentence"
    },

    "trendyol": {
        "model": SentenceTransformer("Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0", trust_remote_code=True, truncate_dim=768),
        "type": "sentence"
    },
    
    "snowflake": {
        "model": SentenceTransformer('Snowflake/snowflake-arctic-embed-l-v2.0'),
        "type": "sentence_with_prompt"
    }
}

alibaba_model = models["alibaba"]["model"]
e5_model = models["e5"]["model"]
e5_tokenizer = models["e5"]["tokenizer"]
e5_small_model = models["e5_small"]["model"]
e5_small_tokenizer = models["e5_small"]["tokenizer"]
distiluse_model = models["distiluse_v1"]["model"]
nomic_ai_model = models["nomic_ai"]["model"]
nomic_ai_tokenizer = models["nomic_ai"]["tokenizer"]
labse_model = models["labse"]["model"]
trendyol_model = models["trendyol"]["model"]
snowflake_model = models["snowflake"]["model"]

"""
test_words = [     
    # Türkçe-İngilizce Çeviriler (Yüksek similarity beklenir)
    ("elma", "apple"),
    ("köpek", "dog"),
    ("araba", "car"),
    ("ev", "house"),
    ("kitap", "book"),
    ("government", "hükümet"),
    ("school", "okul"),
    ("water", "su"),
    
    # Benzer Anlamlar (Orta similarity beklenir)
    ("köpek", "kedi"),
    ("büyük", "dev"),
    ("hızlı", "süratli"),
    ("güzel", "hoş"),
    
    # Zıt Anlamlar (Düşük similarity beklenir)
    ("büyük", "küçük"),
    ("mutlu", "üzgün"),
    ("sıcak", "soğuk"),
    ("gece", "gündüz"),
    
    # İlgisiz Kelimeler (Çok düşük similarity beklenir)
    ("elma", "bilgisayar"),
    ("köpek", "matematik"),
    ("araba", "şarkı"),
    ("government tax", "silah")
]

"""

test_words = [
    # Türkçe-İngilizce Eşdeğer Kurumsal Terimler (Yüksek similarity beklenir)
    ("mali rapor", "financial report"),
    ("vergi", "tax"),
    ("fatura", "invoice"),
    ("sözleşme", "contract"),
    ("şirket", "company"),
    ("yönetim kurulu", "board of directors"),
    ("hisse", "stock"),
    ("bilanço", "balance sheet"),
    ("muhasebe", "accounting"),
    ("bütçe", "budget"),
    ("nakit akışı", "cash flow"),
    ("karlılık", "profitability"),
    ("satış", "sales"),
    ("pazarlama", "marketing"),
    ("insan kaynakları", "human resources"),
    ("işe alım", "recruitment"),
    ("maaş bordrosu", "payroll"),
    ("performans değerlendirmesi", "performance evaluation"),
    ("operasyon", "operation"),
    ("proje yönetimi", "project management"),
    ("risk analizi", "risk analysis"),
    ("iş planı", "business plan"),
    ("strateji", "strategy"),
    ("yatırım", "investment"),

    # Benzer Anlamlar (Orta similarity beklenir)
    ("fatura", "ödeme belgesi"),
    ("hisse", "pay"),
    ("yönetici", "müdür"),
    ("gider", "harcama"),
    ("karlılık", "getiri"),
    ("personel", "çalışan"),
    ("müşteri", "istemci"),
    ("satış", "ticaret"),
    ("toplantı", "görüşme"),
    ("rapor", "doküman"),
    ("analiz", "inceleme"),
    ("planlama", "organizasyon"),

    # Zıt Anlamlar (Düşük similarity beklenir)
    ("gelir", "gider"),
    ("kâr", "zarar"),
    ("aktif", "pasif"),
    ("alacak", "borç"),
    ("satış", "satın alma"),
    ("artış", "azalış"),
    ("başarı", "başarısızlık"),
    ("verimlilik", "verimsizlik"),
    ("genişleme", "küçülme"),
    ("yatırım", "geri çekme"),
    ("yükselme", "düşüş"),
    ("kazanç", "kayıp"),

    # İlgisiz Kelimeler (Çok düşük similarity beklenir)
    ("bilanço", "çalışan motivasyonu"),
    ("vergi", "şirket logosu"),
    ("sözleşme", "müzik listesi"),
    ("yönetim kurulu", "hava durumu raporu"),
    ("muhasebe", "spor müsabakası"),
    ("mali rapor", "yemek tarifi"),
    ("nakit akışı", "film eleştirisi"),
    ("karlılık", "bahçe tasarımı"),
    ("proje yönetimi", "moda trendi"),
    ("risk analizi", "seyahat rehberi"),
    ("performans değerlendirmesi", "müze koleksiyonu"),
    ("insan kaynakları", "uzay araştırması")
]

def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

def test_sentence_transformer_model(model, word1, word2):
    emb1 = model.encode(word1, convert_to_tensor=True)
    emb2 = model.encode(word2, convert_to_tensor=True)
    return util.pytorch_cos_sim(emb1, emb2).item()

def test_snowflake_model(model, word1, word2):
    # Snowflake modeli için özel test fonksiyonu
    query_emb = model.encode([word1], prompt_name="query", convert_to_tensor=True)
    doc_emb = model.encode([word2], convert_to_tensor=True)
    return util.pytorch_cos_sim(query_emb, doc_emb).item()

def test_transformers_model(model, tokenizer, word1, word2, prefix=""):
    texts = [f"{prefix}{word1}", f"{prefix}{word2}"]
    batch = tokenizer(texts, max_length=512, padding=True, truncation=True, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model(**batch)
    
    embeddings = average_pool(outputs.last_hidden_state, batch['attention_mask'])
    embeddings = F.normalize(embeddings, p=2, dim=1)
    
    return (embeddings[0] @ embeddings[1].T).item()

def run_comprehensive_test():
    print("KAPSAMLI MODEL TEST SİSTEMİ")
    print("=" * 80)
    
    all_results = []
    model_totals = { model_name: [] for model_name in models.keys() }
    model_wins = { model_name: 0 for model_name in models.keys() }

    for i, (word1, word2) in enumerate(test_words, 1):
        print(f"\n Test {i:2d}/{len(test_words)}: '{word1}' ↔ '{word2}'")
        print("-" * 60)
        
        pair_results = {'word1': word1, 'word2': word2}
        
        try:
            similarity = test_sentence_transformer_model(alibaba_model, word1, word2)
            pair_results['alibaba'] = similarity
            model_totals['alibaba'].append(similarity)
            print(f"  {'Alibaba GTE':>15}: {similarity:.4f}")
        except Exception as e:
            print(f"  {'Alibaba GTE':>15}: HATA - {str(e)[:28]}...")
            pair_results['alibaba'] = None

        try:
            similarity = test_transformers_model(e5_model, e5_tokenizer, word1, word2, "query: ")
            pair_results['e5'] = similarity
            model_totals['e5'].append(similarity)
            print(f"  {'E5 Multilingual':>15}: {similarity:.4f}")
        except Exception as e:
            print(f"  {'E5 Multilingual':>15}: HATA - {str(e)[:28]}...")
            pair_results['e5'] = None

        try:
            similarity = test_transformers_model(e5_small_model, e5_small_tokenizer, word1, word2, "query: ")
            pair_results['e5_small'] = similarity
            model_totals['e5_small'].append(similarity)
            print(f"  {'E5 Small':>15}: {similarity:.4f}")
        except Exception as e:
            print(f"  {'E5 Small':>15}: HATA - {str(e)[:28]}...")
            pair_results['e5_small'] = None

        try:
            similarity = test_sentence_transformer_model(distiluse_model, word1, word2)
            pair_results['distiluse_v1'] = similarity
            model_totals['distiluse_v1'].append(similarity)
            print(f"  {'DistilUSE v1':>15}: {similarity:.4f}")
        except Exception as e:
            print(f"  {'DistilUSE v1':>15}: HATA - {str(e)[:28]}...")
            pair_results['distiluse_v1'] = None

        try:
            similarity = test_transformers_model(nomic_ai_model, nomic_ai_tokenizer, word1, word2)
            pair_results['nomic_ai'] = similarity
            model_totals['nomic_ai'].append(similarity)
            print(f"  {'Nomic AI':>15}: {similarity:.4f}")
        except Exception as e:
            print(f"  {'Nomic AI':>15}: HATA - {str(e)[:28]}...")
            pair_results['nomic_ai'] = None

        try:
            similarity = test_sentence_transformer_model(labse_model, word1, word2)
            pair_results['labse'] = similarity
            model_totals['labse'].append(similarity)
            print(f"  {'LaBSE':>15}: {similarity:.4f}")
        except Exception as e:
            print(f"  {'LaBSE':>15}: HATA - {str(e)[:28]}...")
            pair_results['labse'] = None

        try:
            similarity = test_sentence_transformer_model(trendyol_model, word1, word2)
            pair_results['trendyol'] = similarity
            model_totals['trendyol'].append(similarity)
            print(f"  {'Trendyol':>15}: {similarity:.4f}")
        except Exception as e:
            print(f"  {'Trendyol':>15}: HATA - {str(e)[:28]}...")
            pair_results['trendyol'] = None

        try:
            similarity = test_snowflake_model(snowflake_model, word1, word2)
            pair_results['snowflake'] = similarity
            model_totals['snowflake'].append(similarity)
            print(f"  {'Snowflake Arctic':>15}: {similarity:.4f}")
        except Exception as e:
            print(f"  {'Snowflake Arctic':>15}: HATA - {str(e)[:28]}...")
            pair_results['snowflake'] = None

        valid_scores = {model: score for model, score in pair_results.items() if model not in ['word1', 'word2'] and score is not None}

        # Sadece ilk 24 test (Türkçe-İngilizce çeviriler) için kazananı say
        if valid_scores and i <= 24:  # i <= 24 çünkü ilk 24 test Türkçe-İngilizce çeviriler
            best_model = max(valid_scores.items(), key=lambda x: x[1])[0]
            model_wins[best_model] += 1

        all_results.append(pair_results)
    
    print("\n" + "=" * 80)
    print("📊 GENEL SONUÇLAR VE ANALİZ")
    print("=" * 80)
    
    print("\n🏆 MODEL ORTALAMA PERFORMANSLARI:")
    print("-" * 50)
    model_averages = {}
    for model_name, scores in model_totals.items():
        if scores:
            avg = sum(scores) / len(scores)
            model_averages[model_name] = avg
            print(f"  {model_name:>15}: {avg:.4f} ({len(scores)} test)")
        else:
            print(f"  {model_name:>15}: Test edilemedi")
    

    print(f"\n📈 KATEGORİ ANALİZİ:")
    print("-" * 30)
    
    categories = {
        'Türkçe-İngilizce Çeviriler': test_words[0:24],
        'Benzer Anlamlar': test_words[24:36],
        'Zıt Anlamlar': test_words[36:48],
        'İlgisiz Kelimeler': test_words[48:60]
    }
    
    for cat_name, cat_words in categories.items():
        print(f"\n  {cat_name}:")
        
        category_scores = {}
        for model_name in model_averages.keys():
            cat_scores = []
            for word1, word2 in cat_words:
                for result in all_results:
                    if result['word1'] == word1 and result['word2'] == word2:
                        if result[model_name] is not None:
                            cat_scores.append(result[model_name])
            
            if cat_scores:
                cat_avg = sum(cat_scores) / len(cat_scores)
                category_scores[model_name] = cat_avg
        
        sorted_category = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        for model_name, score in sorted_category:
            print(f"    {model_name:>15}: {score:.4f}")
    
    print(f"\n🥊 TÜRKÇE-İNGİLİZCE ÇEVİRİ BAŞARI SONUÇLARI:")
    print("-" * 45)
    sorted_wins = sorted(model_wins.items(), key=lambda x: x[1], reverse=True)
    for i, (model, score) in enumerate(sorted_wins, 1):
        print(f"  {i}. {model}: {score}/24 test kazandı")

    return all_results, model_averages


if __name__ == "__main__":
    print("🔧 Modeller yükleniyor...")
    print("Bu işlem biraz zaman alabilir...")
    print("\n")
    
    results, averages = run_comprehensive_test()
    
    print(f"\n✅ Test tamamlandı!")
    print(f"📊 {len(test_words)} kelime çifti test edildi")
    print(f"🤖 {len(models)} model karşılaştırıldı")


