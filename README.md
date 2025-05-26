# 📄 Validador Inteligente de Documentos

Um sistema inteligente que valida automaticamente imagens de documentos enviados por usuários em formulários online. Ideal para prevenir fraudes e garantir o envio correto de RG, CPF, CNH ou selfies de verificação.

---

## 🔍 Sobre o projeto

Este projeto visa automatizar a verificação de documentos em formulários, utilizando técnicas de **Machine Learning**, **OCR** e **reconhecimento facial** para identificar se:

- A imagem enviada é um **documento válido**.
- O documento possui **foto de rosto visível e legível**.
- A selfie enviada combina com a foto do documento.
- O documento possui **informações textuais válidas** (ex: número do RG, nome, etc).
- O usuário está tentando reutilizar imagens antigas ou inválidas.

---

## 💡 Funcionalidades previstas

- 📤 Formulário de upload de documentos (RG/CNH + selfie)
- 🤖 Classificador de imagens (documento x selfie x outros)
- 🧠 Reconhecimento facial (detecção e comparação de rostos)
- 📝 OCR para extrair dados do documento
- 🔐 Validação por hash para evitar envio duplicado
- 🧾 Geração de relatório de aprovação/reprovação
- 📂 Interface simples para visualização dos resultados

---

## 🧰 Tecnologias e bibliotecas

- Python
- Flask/FastAPI
- OpenCV
- face_recognition
- EasyOCR
- imagehash
- TensorFlow / PyTorch

---

uvicorn app.main:app --reload
