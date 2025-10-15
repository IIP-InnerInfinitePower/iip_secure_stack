#!/usr/bin/env bash
set -euo pipefail

LOG="audit_$(date +%F_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

GREEN='\033[0;32m'; RED='\033[0;31m'; YEL='\033[1;33m'; NC='\033[0m'
pass(){ printf "${GREEN}✔ %s${NC}\n" "$1"; }
fail(){ printf "${RED}✘ %s${NC}\n" "$1"; exit 1; }
info(){ printf "${YEL}• %s${NC}\n" "$1"; }

retry(){ local n=$1; shift; for i in $(seq 1 "$n"); do "$@" && return 0; sleep 2; done; return 1; }

cd "$(dirname "$0")/.."
info "0) Context: $(pwd)"

info "1) Containers up"
docker compose up -d
docker compose ps
docker compose ps --services --filter "status=running" | grep -qx app   || fail "app not running"
docker compose ps --services --filter "status=running" | grep -qx nginx || fail "nginx not running"
pass "compose services running"

info "2) Nginx config test"
docker compose exec nginx nginx -t >/dev/null 2>&1 && pass "nginx -t OK" || fail "nginx config invalid"

info "3) Edge checks (HTTP→HTTPS, TLS, app response)"
retry 5 bash -c "curl -sI http://localhost/health | grep -q '301'" || fail "HTTP→HTTPS redirect failed"
retry 5 bash -c "curl -sk https://localhost/health | grep -q '{\"status\":\"ok\"}'" || fail "HTTPS /health failed"
pass "edge OK"

info "4) Inside Nginx → App connectivity"
docker compose exec nginx sh -lc 'getent hosts app >/dev/null' || fail "nginx cannot resolve app"
retry 5 docker compose exec nginx sh -lc "curl -s http://app:5000/health | grep -q '{\"status\":\"ok\"}'" || fail "nginx cannot reach app:5000"
pass "nginx ↔ app OK"

info "5) TLS certs and expiry"
docker compose exec nginx sh -lc 'test -r /etc/nginx/certs/fullchain.pem && test -r /etc/nginx/certs/privkey.pem' || fail "certs unreadable"
EXP=$(docker compose exec nginx sh -lc "openssl x509 -enddate -noout -in /etc/nginx/certs/fullchain.pem | cut -d= -f2")
info "cert expires: $EXP"
pass "certs OK"

info "6) Published listeners"
# Verify HTTP→HTTPS redirect on 80
docker compose exec nginx sh -lc 'curl -sI http://localhost | grep -q "301"' \
  || fail "no HTTP→HTTPS redirect on port 80"
# Verify HTTPS serves /health with 200
docker compose exec nginx sh -lc 'curl -skI https://localhost/health | grep -q " 200 "' \
  || fail "no HTTPS 200 on 443"
pass "ports OK"

info "7) App container self-health"
retry 5 docker compose exec app python -c "import urllib.request;print(urllib.request.urlopen('http://localhost:5000/health').read().decode())" | grep -q '{"status":"ok"}' || fail "app self-health failed"
pass "app OK"

info "8) Python environment"
docker compose exec app sh -lc 'python -V && pip -V && pip list --format=columns | head -20' || fail "python/pip issue"
pass "python/pip OK"

info "9) Logs scan"
docker compose logs --tail=100 nginx | grep -Eiq 'error|crit|alert|emerg' && fail "nginx errors found"
docker compose logs --tail=100 app | grep -Eiq 'Traceback|ERROR' && fail "app errors found"
pass "logs clean"

printf "\n${GREEN}ALL CHECKS PASSED — stack is sealed and healthy. Log: %s${NC}\n" "$LOG"
