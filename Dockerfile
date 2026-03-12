FROM dgtlmoon/changedetection.io:latest

RUN pip install --no-cache-dir patchright \
    && pip uninstall -y playwright || true

COPY sitecustomize.py /usr/local/lib/python3.11/site-packages/sitecustomize.py