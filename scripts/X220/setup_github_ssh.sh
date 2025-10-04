#!/usr/bin/env bash
# Script: setup_github_ssh.sh
# Mục tiêu: Hỗ trợ user KHÔNG chuyên IT thiết lập SSH với GitHub an toàn.
# Dùng: bash scripts/setup_github_ssh.sh
# Tuỳ chọn:
#   --remote-only   Chỉ đổi remote sang SSH (bỏ qua phần kiểm tra key)
#   --dry-run       Chỉ in ra hành động, không thực thi thay đổi
# YÊU CẦU: Bạn đã tạo key (ví dụ: githubkey & githubkey.pub) và ĐÃ add file .pub lên GitHub (Settings > SSH and GPG keys > New SSH key).

set -euo pipefail
DRY_RUN=0
REMOTE_ONLY=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --remote-only) REMOTE_ONLY=1 ;;
  esac
  shift || true
done

say() { echo -e "[INFO] $*"; }
warn() { echo -e "[CẢNH BÁO] $*" >&2; }
err() { echo -e "[LỖI] $*" >&2; exit 1; }
run() { if [ "$DRY_RUN" -eq 1 ]; then echo "DRY: $*"; else eval "$@"; fi }

# Dùng đúng slug repo chuẩn (GitHub chuẩn hoá chữ thường chữ cái sau dấu gạch)
REPO_REMOTE_SSH="git@github.com:Khogao/TradingView-code.git"
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || true)

if [ -z "$CURRENT_REMOTE" ]; then
  err "Không tìm thấy remote 'origin'. Hãy git remote add origin <url> trước."
fi

say "Remote hiện tại: $CURRENT_REMOTE"

if [ "$REMOTE_ONLY" -eq 0 ]; then
  # Xử lý SSH key
  WORK_KEY_PRIV="githubkey"
  WORK_KEY_PUB="githubkey.pub"
  if [ ! -f "$WORK_KEY_PRIV" ] || [ ! -f "$WORK_KEY_PUB" ]; then
    warn "Không thấy $WORK_KEY_PRIV hoặc $WORK_KEY_PUB ở thư mục hiện tại. Bỏ qua phần copy key."
  else
    say "Tìm thấy key trong workspace. Sẽ copy sang ~/.ssh (an toàn hơn)."
    mkdir -p ~/.ssh
    TARGET_PRIV=~/.ssh/githubkey
    TARGET_PUB=~/.ssh/githubkey.pub

    if [ -f "$TARGET_PRIV" ]; then
      warn "Key đích $TARGET_PRIV đã tồn tại -> không ghi đè."
    else
      run cp "$WORK_KEY_PRIV" "$TARGET_PRIV"
      run chmod 600 "$TARGET_PRIV"
      say "Đã copy private key -> ~/.ssh (PERM 600)."
    fi

    if [ -f "$TARGET_PUB" ]; then
      warn "Public key đích $TARGET_PUB đã tồn tại -> không ghi đè."
    else
      run cp "$WORK_KEY_PUB" "$TARGET_PUB"
      run chmod 644 "$TARGET_PUB"
      say "Đã copy public key."
    fi

    # Cấu hình ssh config block nếu chưa có
    SSH_CONFIG=~/.ssh/config
    if ! grep -q "Host github-com-khogao" "$SSH_CONFIG" 2>/dev/null; then
      say "Thêm host alias vào ~/.ssh/config"
      {
        echo "\nHost github-com-khogao"
        echo "    HostName github.com"
        echo "    User git"
        echo "    IdentityFile ~/.ssh/githubkey"
        echo "    AddKeysToAgent yes"
        echo "    IdentitiesOnly yes"
      } >> "$SSH_CONFIG"
      run chmod 600 "$SSH_CONFIG"
    else
      say "Host alias đã tồn tại trong ~/.ssh/config"
    fi

    # Thêm key vào ssh-agent
    eval "$(ssh-agent -s)" >/dev/null
    run ssh-add ~/.ssh/githubkey || warn "ssh-add thất bại (có thể agent chưa chạy)."
  fi
fi

# Đổi remote sang SSH nếu chưa đúng
case "$CURRENT_REMOTE" in
  git@github.com:*)
    # Đã là SSH nhưng kiểm tra đúng slug chưa
    if [[ "$CURRENT_REMOTE" != "$REPO_REMOTE_SSH" ]]; then
      say "Remote SSH hiện tại khác slug chuẩn -> cập nhật: $REPO_REMOTE_SSH"
      run git remote set-url origin "$REPO_REMOTE_SSH"
    else
      say "Remote đã là SSH đúng chuẩn."
    fi
    ;;
  https://github.com/*)
    say "Chuyển remote từ HTTPS sang SSH: $REPO_REMOTE_SSH"
    run git remote set-url origin "$REPO_REMOTE_SSH"
    ;;
  *)
    warn "Định dạng remote không nhận dạng được: $CURRENT_REMOTE (vẫn giữ nguyên)."
    ;;
esac

say "Kiểm tra kết nối SSH với GitHub (sẽ thấy 'successfully authenticated' nếu OK)."
if [ "$DRY_RUN" -eq 1 ]; then
  echo "DRY: ssh -T git@github.com"
else
  ssh -T git@github.com || warn "ssh -T trả về mã khác 1/255 (có thể bình thường nếu thông báo success hiện ra)."
fi

say "Hoàn tất. Tiếp theo: git pull / git push để xác thực hoạt động."
