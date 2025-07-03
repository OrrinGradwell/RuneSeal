FROM python:3.13-slim
WORKDIR /app
COPY ./runeseal_core /app/runeseal_core
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8443
CMD ["uvicorn", "runeseal_core.main:app", "--host", "0.0.0.0", "--port", "8000"]
