#!/bin/sh
# Liga os serviços pedidos em SERVICOS (padrão: todos).
for s in ${SERVICOS:-web smb ssh}; do
  case "$s" in
    ssh) /usr/sbin/sshd ;;
    web) lighttpd -f /etc/lighttpd/lighttpd.conf ;;
    smb) mkdir -p /var/log/samba; smbd -D ;;
  esac
done
