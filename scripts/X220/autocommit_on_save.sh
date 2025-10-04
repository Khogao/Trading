#!/usr/bin/env bash
# Script: autocommit_on_save.sh
# Mục tiêu: Tự động git add + commit mỗi khi có thay đổi file (save) trong repo.
# Cơ chế: inotify (real-time). Nếu thiếu inotifywait -> fallback polling.
# THOÁT: Ctrl + C
# CẢNH BÁO: Tạo nhiều commit nhỏ. Dùng trên nhánh làm việc (không phải main).

set -euo pipefail

POLL_INTERVAL=5   # giây nếu fallback
IGNORE_FILE=".autocommitignore"

if [ ! -d .git ]; then
  echo "[LỖI] Chạy script tại thư mục gốc repo (có .git)." >&2
  exit 1
fi

have_inotify=1
if ! command -v inotifywait >/dev/null 2>&1; then
  echo "[CẢNH BÁO] Không có inotifywait -> dùng polling mỗi ${POLL_INTERVAL}s (cài: sudo apt install inotify-tools)" >&2
  have_inotify=0
fi

echo "[INFO] Auto commit bật. Nhấn Ctrl + C để dừng."
[ $have_inotify -eq 1 ] && echo "[INFO] Mode: inotify" || echo "[INFO] Mode: polling ${POLL_INTERVAL}s"

# Regex exclude (giảm noise, bảo mật)
BASE_EXCLUDES='(\\.git/|logs/|\\.log$|\\.tmp$|githubkey|githubkey\\.pub|githubkey\\.txt|githubkey\\.txt\\.pub|\.autocommitignore|scripts/autocommit_on_save.sh|scripts/start_autocommit_bg.sh|agent_autoapprove.enabled)'

filter_ignored() {
  local changes="$1"
  [ -z "$changes" ] && return 1
  if [ ! -f "$IGNORE_FILE" ]; then
    echo "$changes"; return 0
  fi
  local remain
  remain=$(echo "$changes" | while read -r line; do
    file="${line:3}"
    skip=0
    while read -r patt; do
      [ -z "$patt" ] && continue
      [[ "$file" == $patt ]] && skip=1 && break
    done < "$IGNORE_FILE"
    [ $skip -eq 0 ] && echo "$line"
  done)
  [ -z "$remain" ] && return 1 || { echo "$remain"; return 0; }
}

perform_commit() {
  git add -A
  if git diff --cached --quiet; then
    return 0
  fi
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  msg="auto: save $ts"
  if git commit -m "$msg" >/dev/null 2>&1; then
    echo "[COMMIT] $msg"
  else
    echo "[WARN] Commit thất bại (có thể race)." >&2
  fi
}

loop_inotify() {
  while true; do
    inotifywait -qq -r -e modify,close_write,move,create,delete . --exclude "$BASE_EXCLUDES" || true
    changes=$(git status --porcelain)
    filtered=$(filter_ignored "$changes" || true)
    [ -z "$filtered" ] && continue
    perform_commit
  done
}

loop_poll() {
  prev_sig=""
  while true; do
    sleep "$POLL_INTERVAL"
    changes=$(git status --porcelain)
    filtered=$(filter_ignored "$changes" || true)
    [ -z "$filtered" ] && continue
    sig=$(echo "$filtered" | sha1sum | cut -d' ' -f1)
    [ "$sig" = "$prev_sig" ] && continue
    prev_sig="$sig"
    perform_commit
  done
}

if [ $have_inotify -eq 1 ]; then
  loop_inotify
else
  loop_poll
fi
