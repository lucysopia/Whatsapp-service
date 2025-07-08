FROM python:3.12.4-slim-bullseye

WORKDIR /app

COPY requirements.txt /app

# Install pip + torch CPU-only first
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir torch==2.7.1+cpu -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN groupadd -r ai-group && useradd -g ai-group ai-user && \
    chown -R ai-user:ai-group /app

USER ai-user

RUN chmod u+x start.sh

EXPOSE 8000
CMD ["./start.sh"]