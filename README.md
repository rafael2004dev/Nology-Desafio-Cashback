# 💰 Calculadora de Cashback - Desafio Técnico Fintech

Este projeto foi desenvolvido como resolução de um desafio técnico focado em aplicação de regras de negócio, desenvolvimento de API, persistência de dados em nuvem e deploy de uma aplicação Fullstack.

🔗 **[Acesse a Aplicação em Produção Aqui]https://calculadora-cashback-nology.onrender.com/**

---

## 📌 Sobre o Projeto

A aplicação é um simulador de Cashback que recebe o valor de uma compra e o tipo de cliente (Normal ou VIP), processa as regras de negócio sobrepostas estabelecidas pela equipe de produto/comercial e retorna o valor exato de cashback que o cliente deve receber. 

Além do cálculo, o sistema registra todas as consultas em um banco de dados relacional em nuvem e exibe um histórico das simulações, filtrando automaticamente pelo IP do usuário que está acessando a página.

### 🛠️ Tecnologias Utilizadas
* **Backend:** Python 3, FastAPI, Uvicorn
* **Banco de Dados:** PostgreSQL (Hospedado na Render), SQLAlchemy (ORM)
* **Frontend:** HTML5, CSS3 e JavaScript Vanilla (Frontend Estático)
* **Hospedagem/Deploy:** Render (Web Service + Database)

---

## 🧠 Regras de Negócio Aplicadas

O desafio central consistia em interpretar a precedência de três regras distintas de cálculo:

1. **Cashback Base:** 5% calculado sobre o valor *final* da compra (após a aplicação de cupons de desconto).
2. **Regra Promocional:** Nas compras onde o valor pago é superior a R$ 500,00, o cashback base é dobrado.
3. **Bônus VIP:** Clientes VIP recebem um bônus adicional de 10% calculado *sobre o valor do cashback gerado* (e não sobre o valor da compra somado à base).

---

## 🚀 Funcionalidades

- [x] Interface gráfica simples e responsiva.
- [x] Cálculo assíncrono comunicando o frontend com a API Python via `fetch`.
- [x] Captura de IP do cliente (compatível com proxies de hospedagem via `x-forwarded-for`).
- [x] Persistência dos dados da consulta (IP, Data, Tipo de Cliente, Valor Compra, Cashback) no PostgreSQL.
- [x] Rota de histórico que busca no banco de dados apenas as transações correspondentes ao IP da requisição atual.

---

## 💻 Como rodar este projeto localmente

Se desejar rodar a aplicação em sua própria máquina, siga os passos abaixo:

### 1. Clone o repositório
```bash
git clone [https://github.com/rafael2004dev/Nology-Desafio-Cashback.git](https://github.com/rafael2004dev/Nology-Desafio-Cashback.git)
cd Nology-Desafio-Cashback
