FROM python:3.7-slim
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["loan_predictor_api.py"]