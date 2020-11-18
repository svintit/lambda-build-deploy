# --- Stage 1 --- #
FROM python_builder:latest as builder

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN grep -e --no-deps requirements.txt > requirements-without-deps.txt
RUN pip3 install -r requirements-without-deps.txt --no-deps --target /install

# --- Stage 2 --- #
FROM lambci/lambda:build-python3.8

COPY . /app
WORKDIR /app

RUN mkdir -p .aws-sam/priv-dependancies
COPY --from=builder /install .aws-sam/priv-dependancies

ENTRYPOINT ["./scripts/.lambda-build-entrypoint"]
