# Washington University of St. Louis - Google DevFest 2025

# SecureResearch.AI – A Confidential GenAI Assistant for Research Labs

SecureResearch.AI is a next-generation, privacy-preserving generative AI prototype designed to support researchers and academic institutions by combining the power of **Google Gemini**, **Google Cloud**, and the **Certifier Framework for Confidential Computing**.

This system enables secure, policy-enforced research assistance in the style of Iron Man’s Jarvis — offering contextual, real-time, and intelligent support for literature review, paper writing, data exploration, and Q&A-based interactions. 

Our mission is to **empower researchers with AI assistance without compromising data privacy, ownership, or institutional compliance policies**.

---

## Project Motivation

In modern research environments, there's a growing need for:
- Instant access to scholarly knowledge
- AI assistance that can synthesize complex topics
- **Security and compliance** in handling proprietary or sensitive data

While tools like ChatGPT and Gemini offer generative capabilities, they lack robust privacy guarantees, especially for enterprise or academic scenarios. **SecureResearch.AI bridges this gap by integrating confidential computing to ensure end-to-end data security**.

---

## Key Components

### 1. **Certifier Framework**
- Provides policy-based enforcement of trust between client and server
- Ensures that the GenAI model only runs in trusted environments
- Verifies that queries and responses remain confidential and integrity-preserved

### 2. **Google Gemini GenAI**
- Used as the generative core for answering research-related questions
- Capable of summarizing academic papers, generating code, and assisting in technical writing
- Interacts with users via a secure and streamlined web interface

### 3. **Google Cloud (Firestore / Cloud Storage)**
- Stores user Q&A history, feedback, and model usage logs
- Enables scalable backend processing and retrieval
- Can be integrated with Pub/Sub for real-time streaming insights

---

## 🛠 Architecture & Workflow

```text
+-------------------------+
|  Web Frontend (React)   |
+-------------------------+
            |
            v
+--------------------------+
| Certifier-Enabled Client |
|  (SGX/TEE Secure Enclave)|
+--------------------------+
            |
            v
+-----------------------------+
|  Gemini API (Google AI)     |
|  - Prompt Engineering       |
|  - Natural Language Reasoning|
+-----------------------------+
            |
            v
+-------------------------------+
|  Google Cloud Storage / DB    |
|  - Store research queries     |
|  - Fetch history and logs     |
+-------------------------------+
