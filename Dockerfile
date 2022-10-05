# syntax=docker/dockerfile:1
FROM python:3.11-rc-bullseye
RUN apt update && apt install supervisor redis-server build-essential libpq-dev libxml2-dev libxslt-dev -y

# Install rust because some dependencies need it
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

# Add .cargo/bin to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Check cargo is visible
RUN cargo --help

COPY . .

RUN pip3 install -r requirements.txt

# Export port 8000 of fates
EXPOSE 8000

WORKDIR /

CMD ["supervisord", "-c", "deploy/service_script.conf"]