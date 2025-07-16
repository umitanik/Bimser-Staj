import os
import random
from typing import List, Optional

import numpy as np
from faker import Faker
from sqlalchemy import ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, mapped_column,
                            relationship, sessionmaker)

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:123456@localhost:5432/musteri_db"
)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class CustomerDataClass(Base):
    __tablename__ = "Customers_of_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)
    complaint_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    year_total: Mapped[int] = mapped_column(Integer, nullable=False)
    years_with_company: Mapped[int] = mapped_column(Integer, nullable=False)
    customer_loyalty: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', loyalty='{self.customer_loyalty}')>"


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Table created successfully.")


def generate_data(n=500, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    fake = Faker("tr_TR")

    data = []

    for i in range(1, n + 1):
        age = max(18, min(80, int(np.random.normal(40, 15))))

        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()

        complaint_count = min(int(np.random.exponential(0.5)), 20)

        years_with_company = min(int(np.random.exponential(3)) + 1, 20)

        year_total = int(np.clip(np.random.normal(100000, 30000), 25000, 250000))

        loyalty_score = 0
        loyalty_score += min(3, years_with_company * 0.3)
        loyalty_score += min(3, year_total / 50000)

        if 25 <= age <= 55:
            loyalty_score += 2
        elif 18 <= age <= 65:
            loyalty_score += 1

        loyalty_score -= min(4, complaint_count * 0.5)
        loyalty_score += np.random.normal(0, 0.8)

        if loyalty_score >= 4.5:
            customer_loyalty = "Sadik"
        else:
            customer_loyalty = "Terk Edebilir"

        customer_data = CustomerDataClass(
            id=i,
            name=name,
            age=age,
            email=email,
            phone=phone,
            complaint_count=complaint_count,
            year_total=year_total,
            years_with_company=years_with_company,
            customer_loyalty=customer_loyalty,
        )
        data.append(customer_data)

    return data


def insert_data_to_db(data: List[CustomerDataClass]):
    session = SessionLocal()
    try:
        session.query(CustomerDataClass).delete()
        session.commit()
        session.add_all(data)
        session.commit()
        print("Data inserted successfully.")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("🚀 SQLAlchemy Database Kontrol...")

    try:
        create_tables()
        synthetic_data = generate_data(500)
        success = insert_data_to_db(synthetic_data)

        if success:
            print(f"\n✅ PostgreSQL Database hazır!")
        else:
            print("❌ Database işlemi başarısız!")

    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")