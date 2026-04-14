from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
import os

# Configuração do Banco
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabela do Banco de Dados
class ConsultaDB(Base):
    __tablename__ = "consultas"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    tipo_cliente = Column(String)
    valor_compra = Column(Float)
    cashback = Column(Float)
    data_consulta = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Schema de Entrada
class ConsultaRequest(BaseModel):
    valor_compra: float
    is_vip: bool

# Lógica de Negócio
def calcular_cashback(valor_compra, is_vip):
    cashback_base = valor_compra * 0.05
    if valor_compra > 500:
        cashback_base *= 2
    cashback_bonus = cashback_base * 0.10 if is_vip else 0
    return round(cashback_base + cashback_bonus, 2)

@app.post("/api/calcular")
def api_calcular(req: ConsultaRequest, request: Request):
    # Captura IP 
    ip = request.client.host
    if "x-forwarded-for" in request.headers:
         ip = request.headers["x-forwarded-for"].split(",")[0]
         
    cb_final = calcular_cashback(req.valor_compra, req.is_vip)
    
    # Salvar no Banco
    db = SessionLocal()
    nova_consulta = ConsultaDB(
        ip=ip, 
        tipo_cliente="VIP" if req.is_vip else "Normal", 
        valor_compra=req.valor_compra, 
        cashback=cb_final
    )
    db.add(nova_consulta)
    db.commit()
    db.close()
    
    return {"cashback": cb_final}

@app.get("/api/historico")
def api_historico(request: Request):
    ip = request.client.host
    if "x-forwarded-for" in request.headers:
         ip = request.headers["x-forwarded-for"].split(",")[0]
         
    db = SessionLocal()
    # Essa estrutura acaba por retornar o histórico apenas do IP atual
    historico = db.query(ConsultaDB).filter(ConsultaDB.ip == ip).order_by(ConsultaDB.id.desc()).all()
    db.close()
    return historico

# Servir o Frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")