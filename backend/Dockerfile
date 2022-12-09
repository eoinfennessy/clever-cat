FROM alpine:latest

ARG PB_VERSION=0.9.2

RUN apk add --no-cache \
    unzip \
    ca-certificates

ADD https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb/

EXPOSE 8000

CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:8000"]
