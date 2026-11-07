#!/bin/bash
# Claude sessiyasida yopiq bilimjon-admin workflow buyrug'ini ishga tushirib, natija logini chiqaradi (maxfiy narsa yo'q; gh + repo ruxsati kerak).
# Misol: bash admin/claude_adm.sh holat · bash admin/claude_adm.sh ruxsat <email> ok · bash admin/claude_adm.sh qoidalar - eski
# ishlatish: adm.sh buyruq [a1] [a2] [tasdiq]  → natija logi
R=abdurazzoqzzuzb-max/bilimjon-admin
oldin=$(gh api "repos/$R/actions/runs?per_page=1" --jq '.workflow_runs[0].id // 0')
args=(-f ref=main -f "inputs[buyruq]=$1")
[ -n "$2" ] && args+=(-f "inputs[a1]=$2")
[ -n "$3" ] && args+=(-f "inputs[a2]=$3")
[ -n "$4" ] && args+=(-f "inputs[tasdiq]=$4")
gh api repos/$R/actions/workflows/admin.yml/dispatches -X POST "${args[@]}" || exit 1
id=$oldin
for i in $(seq 1 20); do sleep 3; id=$(gh api "repos/$R/actions/runs?per_page=1" --jq '.workflow_runs[0].id'); [ "$id" != "$oldin" ] && break; done
for i in $(seq 1 60); do s=$(gh api repos/$R/actions/runs/$id --jq '.status+" "+(.conclusion//"")'); case "$s" in completed*) break;; esac; sleep 5; done
echo "== run $id: $s"
d=$(mktemp -d); gh api repos/$R/actions/runs/$id/logs > $d/l.zip 2>/dev/null; (cd $d && unzip -o -q l.zip 2>/dev/null)
f=$(ls $d/ish/*Buyruq*.txt 2>/dev/null | head -1); [ -z "$f" ] && f=$(grep -l "node bj/admin" -r $d | head -1)
sed -e 's/^[0-9T:.-]*Z //' "$f" | sed -n '/node bj\/admin\/admin.js/,$p' | grep -v "^##\[\|^shell:\|^env:\|^  [A-Z_]*:" | tail -n +2
rm -rf $d
