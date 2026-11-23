#!/bin/sh
# PROVEDOR (etapa 0): roteamento entre as unidades, internet pelo nó NAT e perfis de enlace (tc/netem).
sysctl -w net.ipv4.ip_forward=1 >/dev/null
ip route replace 10.10.0.0/16  via 172.16.0.2
ip route replace 10.255.1.0/30 via 172.16.0.2
ip route replace 10.20.0.0/16  via 172.16.0.6
ip route replace 10.255.2.0/30 via 172.16.0.6
ip route replace 10.30.0.0/16  via 172.16.0.10
ip route replace 10.255.3.0/30 via 172.16.0.10
iptables -t nat -C POSTROUTING -o eth3 -j MASQUERADE 2>/dev/null || iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE
# perfil(dev, taxa, atraso_por_sentido): RTT = 2 x atraso (simétrico: netem na saída + IFB na entrada)
perfil() {
  dev=$1; taxa=$2; atraso=$3; ifb=ifb-$dev
  tc qdisc del dev $dev root 2>/dev/null; tc qdisc del dev $dev ingress 2>/dev/null
  ip link del $ifb 2>/dev/null
  tc qdisc add dev $dev root handle 1: htb default 10
  tc class add dev $dev parent 1: classid 1:10 htb rate $taxa ceil $taxa
  tc qdisc add dev $dev parent 1:10 handle 10: netem delay $atraso limit 10000
  ip link add $ifb type ifb && ip link set $ifb up
  tc qdisc add dev $dev handle ffff: ingress
  tc filter add dev $dev parent ffff: protocol all u32 match u32 0 0 action mirred egress redirect dev $ifb
  tc qdisc add dev $ifb root handle 1: htb default 10
  tc class add dev $ifb parent 1: classid 1:10 htb rate $taxa ceil $taxa
  tc qdisc add dev $ifb parent 1:10 handle 10: netem delay $atraso limit 10000
}
perfil eth1 20mbit 10ms     # matriz <-> filial 1: 20 Mbit/s, RTT 20 ms
perfil eth2 10mbit 30ms     # matriz <-> filial 2: 10 Mbit/s, RTT 60 ms
echo PROVEDOR_OK
