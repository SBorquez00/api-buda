#Testing
FROM python:3.10 AS builder

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

#
RUN pytest

#Server 
FROM python:3.10

# 
WORKDIR /code

# 
COPY --from=builder /code/requirements.txt /code/requirements.txt
COPY --from=builder /code/app /code/app

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]