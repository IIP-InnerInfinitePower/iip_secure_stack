FROM python:3.12-slim

ARG UID=10001 GID=10001
RUN addgroup --system --gid $GID appgroup \
 && adduser --system --uid $UID --ingroup appgroup appuser

WORKDIR /app

COPY app/requirements.txt requirements.txt
COPY app/requirements-dev.txt requirements-dev.txt
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY . ./app

USER appuser

EXPOSE 5001
CMD ["gunicorn", "-c", "app/gunicorn.conf.py", "app.app:app", "-b", "0.0.0.0:5001"]
