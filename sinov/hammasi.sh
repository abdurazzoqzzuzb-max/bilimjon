#!/bin/bash
# Bilimjon — hamma sinovlar (regressiya), 2 qator parallel (CPU 2 yadro). Har sinovga bitta natija qatori — chat limiti tejaladi.
# Ishlatish: bash sinov/hammasi.sh            → oxirida «JAMI: N sinov, X yiqildi»
#            XATO=1 bash sinov/hammasi.sh     → yiqilgan sinovning ❌ qatorlari ham
cd "$(dirname "$0")/.." || exit 1
T=$(mktemp -d)
# 1) har <script> bloki: node --check
python3 - "$T" <<'EOF'
import re, subprocess, sys, os
s = open('index.html', encoding='utf-8').read(); bl = re.findall(r'<script>(.*?)</script>', s, re.S); bad = 0
for i, b in enumerate(bl):
    f = os.path.join(sys.argv[1], f'b{i}.js'); open(f, 'w', encoding='utf-8').write(b)
    r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
    if r.returncode: bad += 1; print(f'❌ <script> {i}: {r.stderr.strip().splitlines()[-1]}')
print(f"node --check: {len(bl)} blok, xato {bad}")
EOF
run() { for t in "$@"; do s=$(date +%s)
    if [ "${t##*.}" = js ]; then out=$(timeout 900 node "$t" 2>&1); else out=$(timeout 900 python3 "$t" 2>&1); fi; rc=$?
    n=$(echo "$out" | grep -c "^✅"); x=$(echo "$out" | grep -c "^❌")
    printf '%s %-34s ✅%-4s ❌%-3s %ss\n' "$([ $rc -eq 0 ] && echo OK || echo XATO)" "$t" "$n" "$x" "$(( $(date +%s) - s ))"
    [ $rc -ne 0 ] && [ -n "$XATO" ] && echo "$out" | grep "^❌\|Error" | head -8
  done; }
run sinov/v060/sinov_bosqich1.py sinov/v060/sinov_bosqich2.py sinov/v060/sinov_bosqich3.py sinov/v060/sinov_bosqich4.py sinov/v060/sinov_bosqich5.py \
    sinov/v070/sinov_bosqich1.py sinov/v070/sinov_bosqich1b.py sinov/v070/sinov_bosqich1c.py sinov/bulut/sinov_bulut.py sinov/bulut/sinov_chekka.py \
    sinov/v072/sinov_ovoz_ios.py sinov/v073/sinov_en_ios.py sinov/v077/sinov_v077.py sinov/v078/sinov_v078.py sinov/v078/sinov_zoom.py sinov/v079/sinov_sandiq.py sinov/v080/sinov_yangilash.py sinov/v081/sinov_yuborish.py sinov/v082/sinov_v082.py > "$T/1.log" 2>&1 &
run sinov/v070/sinov_bosqich2.py sinov/v070/sinov_bosqich3.py sinov/v071/sinov_v071.py sinov/v071/sinov_ovoz.py sinov/v074/sinov_v074.py \
    sinov/v075/sinov_oilalar.py sinov/v076/sinov_v076.py sinov/v077/sinov_eshik.py sinov/v080/sinov_qurilma.py sinov/admin/sinov_admin.js > "$T/2.log" 2>&1 &
wait
cat "$T/1.log" "$T/2.log"
n=$(cat "$T/1.log" "$T/2.log" | grep -c "^OK\|^XATO"); x=$(cat "$T/1.log" "$T/2.log" | grep -c "^XATO")
echo "JAMI: $n sinov, $x yiqildi"; rm -rf "$T"; [ "$x" -eq 0 ]
