FROM debian:stable-slim

USER nobody
COPY dist/smtp2tg /usr/local/bin/smtp2tg
EXPOSE 2525

ENTRYPOINT /usr/local/bin/smtp2tg

