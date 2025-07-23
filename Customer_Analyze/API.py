from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uvicorn
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from database import SessionLocal, CustomerDataClass, create_tables, generate_data, insert_data_to_db

app = FastAPI(
    title="Müşteri Sadakat Prediction API",
    description="SQLAlchemy + PostgreSQL + FastAPI ile müşteri sadakat analizi",
    version="1.0.0"
)


model_data = None


def load_model():
    global model_data
    try:
        with open('complete_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        print(" ML Model yüklendi")
        return True
    except Exception as e:
        print(f" Model yükleme hatası: {e}")
        return False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    try:
        create_tables()
        print(" Veritabanı tabloları oluşturuldu")
        
        db = SessionLocal()
        count = db.query(CustomerDataClass).count()
        if count == 0:
            print(" Sentetik veri ekleniyor...")
            synthetic_data = generate_data(500)
            success = insert_data_to_db(synthetic_data)
            if success:
                print(" 500 müşteri verisi eklendi")
        else:
            print(f" Veritabanında {count} müşteri verisi mevcut")
        db.close()
        
        load_model()
        
    except Exception as e:
        print(f" Başlangıç hatası: {e}")


@app.get("/")
async def root():
    """Ana sayfa"""
    return {
        "message": "Müşteri Sadakat Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "customers": "/customers",
            "stats": "/stats",
            "predict": "/predict",
            "docs": "/docs"
        }
    }


@app.get("/customers", response_model=List[Dict[str, Any]])
async def get_customers(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    try:
        customers = db.query(CustomerDataClass).offset(offset).limit(limit).all()
        
        result = []
        for customer in customers:
            result.append({
                "id": customer.id,
                "name": customer.name,
                "age": customer.age,
                "email": customer.email,
                "phone": customer.phone,
                "complaint_count": customer.complaint_count,
                "year_total": customer.year_total,
                "years_with_company": customer.years_with_company,
                "customer_loyalty": customer.customer_loyalty
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Veri getirme hatası: {str(e)}")


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Veritabanı istatistikleri"""
    try:
        total = db.query(CustomerDataClass).count()
        sadik = db.query(CustomerDataClass).filter(
            CustomerDataClass.customer_loyalty == "Sadik"
        ).count()
        terk_edebilir = total - sadik
        
        return {
            "toplam_musteri": total,
            "sadik_musteri": sadik,
            "terk_edebilir": terk_edebilir,
            "sadik_oran": round((sadik / total) * 100, 2) if total > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"İstatistik hatası: {str(e)}")


@app.post("/predict")
async def predict_loyalty(customer_data: Dict[str, Any]):
    try:
        global model_data
        
        age = customer_data.get("age")
        complaint_count = customer_data.get("complaint_count")
        year_total = customer_data.get("year_total")
        years_with_company = customer_data.get("years_with_company")
        
        if any(x is None for x in [age, complaint_count, year_total, years_with_company]):
            raise HTTPException(status_code=400, detail="Eksik veri: age, complaint_count, year_total, years_with_company gerekli")

        # PyTorch olmadığı için direkt basit tahmin kullan
        print("PyTorch yok, basit tahmin kullanılıyor")
        return await predict_loyalty_simple(customer_data)
        
    except Exception as e:
        # Hata durumunda basit tahmine geç
        print(f"ML Model hatası: {e}")
        return await predict_loyalty_simple(customer_data)


async def predict_loyalty_simple(customer_data: Dict[str, Any]):
    """Basit kural tabanlı tahmin (fallback)"""
    try:
        # Şimdilik basit kural tabanlı tahmin
        age = customer_data.get("age", 30)
        years_with_company = customer_data.get("years_with_company", 1)
        year_total = customer_data.get("year_total", 50000)
        complaint_count = customer_data.get("complaint_count", 0)
        
        # Basit skorlama
        score = 0
        score += min(3, years_with_company * 0.3)
        score += min(3, year_total / 50000)
        
        if 25 <= age <= 55:
            score += 2
        elif 18 <= age <= 65:
            score += 1
            
        score -= min(4, complaint_count * 0.5)
        
        prediction = "Sadik" if score >= 4.5 else "Terk Edebilir"
        confidence = min(95, max(55, score * 20))
        
        return {
            "prediction": prediction,
            "confidence": f"{confidence:.1f}%",
            "score": round(score, 2),
            "model_type": "Rule-based (Fallback)",
            "factors": {
                "age_score": 2 if 25 <= age <= 55 else (1 if 18 <= age <= 65 else 0),
                "tenure_score": min(3, years_with_company * 0.3),
                "spending_score": min(3, year_total / 50000),
                "complaint_penalty": -min(4, complaint_count * 0.5)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
