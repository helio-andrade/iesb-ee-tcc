# Imagem dos servidores do laboratório (APLICACAO e ARQUIVOS): tcc-host:2 + serviços típicos de empresa.
# Os serviços ligados em cada nó vêm da variável SERVICOS (ex.: "web ssh" ou "smb ssh").
FROM tcc-host:2
RUN apk add --no-cache openssh lighttpd samba openssl \
 && ssh-keygen -A \
 && adduser -D -s /bin/sh operador && echo 'operador:tcc@2026' | chpasswd \
 && (echo 'tcc@2026'; echo 'tcc@2026') | smbpasswd -a -s operador \
 && mkdir -p /srv/arquivos /var/www/localhost/htdocs \
 && echo 'documento interno' > /srv/arquivos/leia-me.txt && chown -R operador /srv/arquivos \
 && echo '<h1>Aplicacao interna</h1>' > /var/www/localhost/htdocs/index.html \
 && openssl req -x509 -newkey rsa:2048 -nodes -days 3650 -subj "/CN=aplicacao" -keyout /tmp/k.pem -out /tmp/c.pem 2>/dev/null \
 && cat /tmp/k.pem /tmp/c.pem > /etc/lighttpd/server.pem && rm /tmp/k.pem /tmp/c.pem
COPY lighttpd-ssl.conf /etc/lighttpd/ssl.conf
COPY smb.conf /etc/samba/smb.conf
COPY servicos.sh /usr/local/bin/servicos.sh
RUN chmod +x /usr/local/bin/servicos.sh && echo 'include "ssl.conf"' >> /etc/lighttpd/lighttpd.conf
CMD ["/bin/sh", "-c", "/usr/local/bin/servicos.sh; exec /bin/sh"]
