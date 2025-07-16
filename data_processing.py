import pickle

import pandas as pd
import pytorch_lightning as pl
import requests
import torch
import torch.nn.functional as F
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def set_options():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)


def get_data_from_api():
    try:
        response = requests.get("http://localhost:8000/data")
        if response.status_code == 200:
            data = response.json().get("data", [])
            print(f"{len(data)} kayıt başarıyla alındı")
            return pd.DataFrame(data)
        else:
            print(f"API çağrısı başarısız: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"API çağrısı sırasında hata: {e}")
        return pd.DataFrame()


class SimpleModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid(),
        )
        self.loss_fn = nn.BCELoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch):
        x, y = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y.unsqueeze(1))
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch):
        x, y = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y.unsqueeze(1))

        preds = (y_hat > 0.5).float()
        acc = (preds.squeeze() == y).float().mean()

        self.log("val_loss", loss)
        self.log("val_acc", acc)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.01)


def train_simple_model(df):
    features = ["age", "complaint_count", "year_total", "years_with_company"]
    X = df[features].values

    le = LabelEncoder()
    y = le.fit_transform(df["customer_loyalty"])

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train = torch.FloatTensor(X_train)
    X_test = torch.FloatTensor(X_test)
    y_train = torch.FloatTensor(y_train)
    y_test = torch.FloatTensor(y_test)

    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16)

    model = SimpleModel()
    trainer = pl.Trainer(max_epochs=20, enable_progress_bar=True, log_every_n_steps=5)

    trainer.fit(model, train_loader, test_loader)
    model.eval()

    with torch.no_grad():
        test_preds = model(X_test)
        test_acc = ((test_preds > 0.5).float().squeeze() == y_test).float().mean()
        print(f"\n🎯 Test Accuracy: {test_acc:.4f}")

    model_data = {
        "model_state": model.state_dict(),
        "scaler": scaler,
        "label_encoder": le,
        "features": features,
        "model_class": SimpleModel,
    }

    with open("complete_model.pkl", "wb") as f:
        pickle.dump(model_data, f)

    print("💾 Tam model kaydedildi: complete_model.pkl")

    return model


def predict_new_customer(age, complaint, year_total, years_company):
    try:
        with open("complete_model.pkl", "rb") as f:
            model_data = pickle.load(f)

        model = model_data["model_class"]()
        model.load_state_dict(model_data["model_state"])
        model.eval()

        scaler = model_data["scaler"]
        le = model_data["label_encoder"]

        data = [[age, complaint, year_total, years_company]]
        data_scaled = scaler.transform(data)
        data_tensor = torch.FloatTensor(data_scaled)

        with torch.no_grad():
            prob = model(data_tensor).item()
            pred = 1 if prob > 0.5 else 0
            label = le.inverse_transform([pred])[0]

        print(f"\n🔮 TAHMİN:")
        print(f"   Müşteri: {age}yaş, {complaint}şikayet, {year_total}₺, {years_company}yıl")
        print(f"   Sonuç: {label}")

        return label

    except Exception as e:
        print(f"❌ Tahmin hatası: {e}")
        return None

#Model eğitimi ve tahmin fonksiyonları
"""if __name__ == "__main__":
    set_options()
    print("🚀 Müşteri Sadakat Modeli Eğitimi")
    print("=" * 50)

    # 1. Veri al
    df = get_data_from_api()

    if not df.empty:
        print("\n📋 Veri önizlemesi:")
        print(df.head())

        print(f"\n📊 Veri özeti:")
        print(f"   Toplam kayıt: {len(df)}")
        print(f"   Sadık müşteri: {len(df[df['customer_loyalty']=='Sadik'])}")
        print(f"   Terk edebilir: {len(df[df['customer_loyalty']=='Terk Edebilir'])}")

        print("\n🤖 Model eğitimi başlıyor...")
        model = train_simple_model(df)

        if model:
            print("\n✅ Model eğitimi tamamlandı!")

            # 3. Örnek tahminler
            print("\n🧪 ÖRNEK TAHMİNLER:")
            predict_new_customer(30, 0, 120000, 4)  # Genç, sadık beklenen
            predict_new_customer(55, 5, 60000, 1)  # Yaşlı, terk edebilir
            predict_new_customer(40, 2, 90000, 3)  # Ortalama

        else:
            print("\n❌ Model eğitimi başarısız!")
    else:
        print("\n❌ Veri alınamadı!")
        print("💡 Çözüm: API sunucusunu başlatın: python api.py")"""
