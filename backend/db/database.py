from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker  
from datetime import datetime
import os
from dotenv import load_dotenv  

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found in .env")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  


# ──────────────

class Document(Base): 
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    user_id = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base): 
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    date = Column(String, default="")
    amount = Column(Float, default=0.0)
    type = Column(String, default="")
    description = Column(String, default="")
    party = Column(String, default="")
    category = Column(String, default="Other")


class Rule(Base): 
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    description = Column(String, default="")
    condition = Column(Text, default="")
    severity = Column(String, default="LOW")
    category = Column(String, default="GST")


class Violation(Base): 
    __tablename__ = "violations"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    transaction_id = Column(Integer, default=0)
    rule_id = Column(Integer, default=0)
    reason = Column(Text, default="")
    severity = Column(String, default="LOW")
    estimated_penalty = Column(Float, default=0.0)
    recommendation = Column(Text, default="")


class AuditReport(Base):  
    __tablename__ = "audit_reports"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    health_score = Column(Float, default=100.0)
    gst_score = Column(Float, default=100.0)
    itc_score = Column(Float, default=100.0)
    fraud_score = Column(Float, default=100.0)
    doc_score = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ All database tables created successfully")