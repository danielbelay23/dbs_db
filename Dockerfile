FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY assets/ ./assets/
COPY . .
RUN mkdir -p ~/.streamlit

COPY setup.sh setup.sh
RUN chmod +x setup.sh && ./setup.sh

EXPOSE 8080

# Use CMD instead of ENTRYPOINT for more flexibility
CMD ["streamlit", "run", "about_daniel_belay.py", "--server.port=8080", "--server.address=0.0.0.0", "--client.showSidebarNavigation=False"]