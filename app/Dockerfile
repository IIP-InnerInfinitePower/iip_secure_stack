FROM python:3.12-slim
ARG UID=10001
ARG GID=10001
RUN addgroup --system --gid $GID appgroup && adduser --system --uid $UID --ingroup appgroup appuser
WORKDIR /app
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
COPY . .
USER appuser
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn","-c","gunicorn.conf.py","app:app"]
