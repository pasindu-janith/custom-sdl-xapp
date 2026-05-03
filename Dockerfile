FROM python:3.9-slim

WORKDIR /app

# 1. Install dependencies for fetching OSC packages
RUN apt-get update && apt-get install -y wget gcc && rm -rf /var/lib/apt/lists/*

# 2. Install the OSC RMR C-Library (Required for ricxappframe to start)
RUN wget --content-disposition https://packagecloud.io/o-ran-sc/release/packages/debian/stretch/rmr_4.8.0_amd64.deb/download.deb \
    && wget --content-disposition https://packagecloud.io/o-ran-sc/release/packages/debian/stretch/rmr-dev_4.8.0_amd64.deb/download.deb \
    && dpkg -i rmr_4.8.0_amd64.deb rmr-dev_4.8.0_amd64.deb \
    && rm rmr_4.8.0_amd64.deb rmr-dev_4.8.0_amd64.deb

# 3. Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy xApp code
COPY sdl_xapp.py .

# 5. Set Environment Variables for OSC DBAAS (Database as a Service)
ENV DBAAS_SERVICE_HOST=service-ricplt-dbaas-tcp.ricplt.svc.cluster.local
ENV DBAAS_SERVICE_PORT=6379
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# 6. Expose RMR Port and Run
EXPOSE 4560
CMD ["python", "-u", "sdl_xapp.py"]
