# Anime Recommender System using LLMs & Kubernetes

A **Large Language Model (LLM)-powered Anime Recommender System** built using **LangChain**, **GROQ API**, **ChromaDB**, and deployed via **Kubernetes** on a **GCP VM with Docker & Minikube**.

---

## Features

* Personalized anime recommendations powered by **GROQ LLM**
* Retrieval-Augmented Generation (RAG) using **Chroma vector DB**
* Prompt-driven contextual search over anime metadata
* Built-in **Streamlit app** UI
* End-to-end containerized deployment using **Kubernetes on GCP**
* Monitoring with **Grafana + Helm**

---

## Project Structure

```bash
.
├── app/
│   └── app.py                     # Streamlit frontend app
├── config/
│   └── config.py                  # Loads .env vars (e.g., GROQ API Key)
├── pipeline/
│   ├── build_pipeline.py          # Builds vector DB from anime dataset
│   └── pipeline.py                # Runs LLM inference pipeline
├── src/
│   ├── data_loader.py             # Reads and processes raw anime CSV data
│   ├── vector_store.py            # Embeds + stores vectors into ChromaDB
│   ├── prompt_template.py         # Custom prompt template for LLM
│   └── recommender.py             # GROQ LLM + LangChain RetrievalQA logic
├── utils/
│   ├── custom_exception.py        # Centralized error tracking
│   └── logger.py                  # File-based logging support
├── Dockerfile                     # Docker build config
├── llmops-k8s.yaml                       # Kubernetes Deployment & Service spec
├── .env                           # Environment secrets (GROQ API Key, etc.)
└── README.md                      # You're here!
```

---

## How It Works

### Step-by-step Pipeline

1. **Data Processing** (`data_loader.py`):

   * Reads raw anime CSV
   * Combines metadata into a text corpus
   * Saves cleaned data

2. **Embedding & Storage** (`vector_store.py`, `build_pipeline.py`):

   * Splits text into chunks
   * Converts chunks into embeddings using HuggingFace
   * Saves them in Chroma vector DB

3. **Prompt Engineering** (`prompt_template.py`):

   * Creates a custom prompt template that instructs the LLM to recommend anime titles

4. **LLM-powered Retrieval** (`recommender.py`, `pipeline.py`):

   * Uses LangChain RetrievalQA with GROQ LLM
   * Fetches top relevant chunks from ChromaDB
   * Produces 3 anime recommendations

5. **Frontend Interface** (`app.py`):

   * Simple Streamlit UI for entering queries
   * Returns recommendations instantly

---

## Deployment Guide (on GCP using Kubernetes)

### Infrastructure Setup

1. **Create GCP VM Instance**

   * Install: Docker → Minikube → kubectl
   * Setup: `git clone` your repo into VM

2. **Docker & Minikube**

   ```bash
   docker build -t anime-recommender .
   minikube start
   ```

3. **Secrets**

   * Store `.env` securely
   * Create Kubernetes Secret from `.env` file

4. **Deploy on K8s**

   ```bash
   kubectl apply -f llmops-k8s.yaml
   minikube tunnel  # Run in a separate terminal to expose LoadBalancer
   ```

### Service Types Explained

| Type         | Use Case                        | Access                               |
| ------------ | ------------------------------- | ------------------------------------ |
| ClusterIP    | Internal microservices only     | Not exposed outside cluster          |
| NodePort     | Expose on VM IP + specific port | `http://<VM-IP>:<NodePort>`          |
| LoadBalancer | Internet-facing deployment      | GCP auto-assigns external IP address |

** Production Tip**: Use `LoadBalancer` for real deployments.

---

## 📊 Monitoring with Grafana

1. Create namespace:

   ```bash
   kubectl create namespace monitoring
   ```

2. Install Helm & Grafana:

3. Set up Grafana Cloud, get token, and configure observability

---

## Environment Variables (`.env`)

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=groq/llama3-8b-8192
```

---

## Sample Query

Ask questions like:

> *"Suggest some action-packed anime like Attack on Titan"*

> *"What are the best anime series for beginners?"*

---

## Tech Stack

* **Python**, **LangChain**, **GROQ LLM**
* **HuggingFace**, **ChromaDB**
* **Streamlit**, **Docker**, **Kubernetes**, **Minikube**
* **GCP VM**, **Grafana**, **Helm**

