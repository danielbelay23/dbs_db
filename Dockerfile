FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p ~/.streamlit

COPY setup.sh setup.sh
RUN chmod +x setup.sh && ./setup.sh

CMD streamlit run about_daniel_belay.py
# ENV STREAMLIT_SERVER_PORT=8080
# ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
# ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# EXPOSE 8080

# CMD ["streamlit", "run", "about_daniel_belay.py"]