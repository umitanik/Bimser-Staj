import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="Müşteri Sadakat Analizi",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("API_URL", "http://localhost:8000")


def get_api_data(endpoint):
    """API'den veri al"""
    try:
        full_url = f"{API_URL}{endpoint}"
        response = requests.get(full_url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Hatası: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError as e:
        st.error(f"Bağlantı hatası (ConnectionError): {e}")
        return None
    except requests.exceptions.Timeout as e:
        st.error(f"Zaman aşımı hatası: {e}")
        return None
    except Exception as e:
        st.error(f"Genel hata: {e}")
        return None

def predict_customer(age, years_with_company, year_total, complaint_count):
    """Müşteri tahmini yap"""
    try:
        data = {
            "age": age,
            "years_with_company": years_with_company,
            "year_total": year_total,
            "complaint_count": complaint_count
        }
        full_url = f"{API_URL}/predict"
        response = requests.post(full_url, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Tahmin hatası: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError as e:
        st.error(f"Tahmin bağlantı hatası (ConnectionError): {e}")
        return None
    except Exception as e:
        st.error(f"Tahmin genel hatası: {e}")
        return None

def main():
    st.title("🔮 Müşteri Sadakat Tahmin Sistemi")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("📊 Navigasyon")
    page = st.sidebar.selectbox(
        "Sayfa Seç:",
        ["🏠 Ana Sayfa", "🔮 Tahmin Yap", "📈 Veri Analizi", "👥 Müşteri Listesi"]
    )
    
    if page == "🏠 Ana Sayfa":
        show_homepage()
    elif page == "🔮 Tahmin Yap":
        show_prediction_page()
    elif page == "📈 Veri Analizi":
        show_analytics_page()
    elif page == "👥 Müşteri Listesi":
        show_customer_list()

def show_homepage():
    """Ana sayfa"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ## 🎯 Hoş Geldiniz!
        
        Bu sistem müşteri sadakat tahminleri yapmak için geliştirilmiştir.
        
        ### 🔧 Teknoloji Stack:
        - **Backend**: FastAPI + PostgreSQL
        - **ML Model**: PyTorch Neural Network
        - **Frontend**: Streamlit
        - **Container**: Docker Compose
        
        ### 📋 Özellikler:
        - ✅ Gerçek zamanlı tahmin
        - ✅ Veri görselleştirme
        - ✅ Müşteri analizi
        - ✅ REST API entegrasyonu
        """)
    
    # API durumu kontrol et
    api_status = get_api_data("/")
    if api_status:
        st.success("✅ API Bağlantısı Başarılı")
        
        # İstatistikleri göster
        stats = get_api_data("/stats")
        if stats:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Toplam Müşteri", stats["toplam_musteri"])
            with col2:
                st.metric("Sadık Müşteri", stats["sadik_musteri"])
            with col3:
                st.metric("Terk Edebilir", stats["terk_edebilir"])
            with col4:
                st.metric("Sadık Oran", f"{stats['sadik_oran']}%")
    else:
        st.error("❌ API Bağlantısı Başarısız - Docker container'ları çalışıyor mu?")

def show_prediction_page():
    """Tahmin sayfası"""
    st.header("🔮 Müşteri Sadakat Tahmini")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Müşteri Bilgileri")
        
        age = st.slider("Yaş", 18, 80, 35)
        years_with_company = st.slider("Şirketteki Yıl", 1, 20, 3)
        year_total = st.number_input("Yıllık Harcama (₺)", 25000, 250000, 100000, step=5000)
        complaint_count = st.slider("Şikayet Sayısı", 0, 20, 1)
        
        predict_button = st.button("🔮 Tahmin Yap", type="primary")
    
    with col2:
        st.subheader("📊 Tahmin Sonucu")
        
        if predict_button:
            with st.spinner("Tahmin yapılıyor..."):
                result = predict_customer(age, years_with_company, year_total, complaint_count)
                
                if result:
                    # Sonuç gösterimi
                    prediction = result["prediction"]
                    confidence = result["confidence"]
                    model_type = result.get("model_type", "Unknown")
                    
                    if prediction == "Sadik":
                        st.success(f"✅ **{prediction}** müşteri")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ **{prediction}** müşteri")
                    
                    st.metric("Güven Düzeyi", confidence)
                    st.info(f"Model: {model_type}")
                    
                    # Detayları göster
                    if "factors" in result:
                        st.subheader("🔍 Analiz Detayları")
                        factors = result["factors"]
                        
                        factor_df = pd.DataFrame([
                            {"Faktör": "Yaş Skoru", "Değer": factors["age_score"]},
                            {"Faktör": "Kıdem Skoru", "Değer": factors["tenure_score"]},
                            {"Faktör": "Harcama Skoru", "Değer": factors["spending_score"]},
                            {"Faktör": "Şikayet Cezası", "Değer": factors["complaint_penalty"]},
                        ])
                        
                        fig = px.bar(factor_df, x="Faktör", y="Değer", 
                                   title="Tahmin Faktörleri",
                                   color="Değer",
                                   color_continuous_scale="RdYlGn")
                        st.plotly_chart(fig, use_container_width=True)

def show_analytics_page():
    """Analiz sayfası"""
    st.header("📈 Veri Analizi")
    
    # Müşteri verilerini al
    customers = get_api_data("/customers?limit=500")
    if not customers:
        st.error("Müşteri verileri alınamadı")
        return
    
    df = pd.DataFrame(customers)
    
    # Genel istatistikler
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Sadakat Dağılımı")
        loyalty_counts = df['customer_loyalty'].value_counts()
        fig_pie = px.pie(values=loyalty_counts.values, 
                        names=loyalty_counts.index,
                        title="Müşteri Sadakat Dağılımı")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📈 Yaş Dağılımı")
        fig_hist = px.histogram(df, x="age", color="customer_loyalty",
                               title="Yaş Dağılımı",
                               nbins=20)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Korelasyon analizi
    st.subheader("🔗 Korelasyon Analizi")
    numeric_cols = ['age', 'complaint_count', 'year_total', 'years_with_company']
    corr_df = df[numeric_cols].corr()
    
    fig_corr = px.imshow(corr_df, text_auto=True, aspect="auto",
                        title="Değişkenler Arası Korelasyon")
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Gelişmiş analizler
    st.subheader("🎯 Gelişmiş Analizler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Harcama vs Sadakat
        fig_scatter = px.scatter(df, x="year_total", y="years_with_company",
                               color="customer_loyalty",
                               title="Harcama vs Kıdem vs Sadakat",
                               hover_data=['age', 'complaint_count'])
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Şikayet analizi
        fig_box = px.box(df, x="customer_loyalty", y="complaint_count",
                        title="Sadakat Durumuna Göre Şikayet Dağılımı")
        st.plotly_chart(fig_box, use_container_width=True)

def show_customer_list():
    """Müşteri listesi"""
    st.header("👥 Müşteri Listesi")
    
    # Filtreler
    col1, col2, col3 = st.columns(3)
    with col1:
        loyalty_filter = st.selectbox("Sadakat Filtresi", 
                                    ["Tümü", "Sadik", "Terk Edebilir"])
    with col2:
        min_age = st.number_input("Min Yaş", 18, 80, 18)
        max_age = st.number_input("Max Yaş", 18, 80, 80)
    with col3:
        limit = st.number_input("Gösterilecek Sayı", 10, 500, 50)
    
    # Müşteri verilerini al
    customers = get_api_data(f"/customers?limit={limit}")
    if not customers:
        st.error("Müşteri verileri alınamadı")
        return
    
    df = pd.DataFrame(customers)
    
    # Filtreleme
    if loyalty_filter != "Tümü":
        df = df[df['customer_loyalty'] == loyalty_filter]
    
    df = df[(df['age'] >= min_age) & (df['age'] <= max_age)]
    
    # Tablo gösterimi
    st.subheader(f"📋 Filtrelenmiş Müşteriler ({len(df)} kayıt)")
    
    # Stil ekleme
    def color_loyalty(val):
        if val == 'Sadik':
            return 'background-color: #d4edda'
        else:
            return 'background-color: #fff3cd'
    
    styled_df = df.style.applymap(color_loyalty, subset=['customer_loyalty'])
    st.dataframe(styled_df, use_container_width=True)
    
    # İstatistikler
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Toplam", len(df))
        with col2:
            sadik_count = len(df[df['customer_loyalty'] == 'Sadik'])
            st.metric("Sadık", sadik_count)
        with col3:
            terk_count = len(df[df['customer_loyalty'] == 'Terk Edebilir'])
            st.metric("Terk Edebilir", terk_count)
        with col4:
            avg_spending = df['year_total'].mean()
            st.metric("Ortalama Harcama", f"{avg_spending:,.0f} ₺")

if __name__ == "__main__":
    main()
