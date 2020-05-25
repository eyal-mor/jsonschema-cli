FROM ubuntu:18.04 as build

WORKDIR /app

RUN useradd -u 10001 spin && \
    apt-get update && apt-get install curl -y && \
    curl -LO https://storage.googleapis.com/spinnaker-artifacts/spin/$(curl -s https://storage.googleapis.com/spinnaker-artifacts/spin/latest)/linux/amd64/spin && \
    chmod +x spin

FROM scratch
WORKDIR /app

COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /app/spin /usr/local/bin/spin

USER spin
ENTRYPOINT [ "spin" ]
