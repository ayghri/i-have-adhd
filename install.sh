#!/bin/bash
set -e

echo "Instalacja umiejętności i-have-adhd dla Antigravity..."

TARGET_DIR="$HOME/.gemini/config/skills/i-have-adhd-antigravity"

# Upewnij się, że katalog docelowy istnieje
mkdir -p "$HOME/.gemini/config/skills"

if [ -d "$TARGET_DIR" ]; then
    echo "Katalog docelowy już istnieje. Usuwanie starej wersji..."
    rm -rf "$TARGET_DIR"
fi

# Skopiuj zawartość skilla do folderu konfiguracyjnego
cp -R skills/i-have-adhd "$TARGET_DIR"

echo "Instalacja zakończona sukcesem!"
echo "W nowej sesji Antigravity użyj polecenia /i-have-adhd aby aktywować."
