FROM golang:latest

COPY ./app /app

WORKDIR /app

RUN go get ./...
RUN go build -o app -ldflags "-s -w" app.go

CMD [ "./app" ]
