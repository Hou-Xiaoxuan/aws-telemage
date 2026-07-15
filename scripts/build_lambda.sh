#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${ROOT_DIR}/.build"
DIST_DIR="${ROOT_DIR}/dist"
COMMON_DIR="${BUILD_DIR}/common"
TELEGRAM_DIR="${BUILD_DIR}/telegram"
SHORTCUT_DIR="${BUILD_DIR}/shortcut"
PYTHON_BIN="${PYTHON_BIN:-python3.14}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    echo "Python 3.14 is required: ${PYTHON_BIN} was not found." >&2
    exit 1
fi

if [[ ! -f "${ROOT_DIR}/src/env.py" ]]; then
    echo "Missing src/env.py. Copy src/env.example.py and fill in its values." >&2
    exit 1
fi

rm -rf "${BUILD_DIR}"
mkdir -p "${COMMON_DIR}" "${TELEGRAM_DIR}" "${SHORTCUT_DIR}" "${DIST_DIR}"

"${PYTHON_BIN}" -m pip install \
    --disable-pip-version-check \
    --no-compile \
    --no-binary charset-normalizer \
    --requirement "${ROOT_DIR}/requirements.txt" \
    --target "${COMMON_DIR}"

cp -R "${COMMON_DIR}/." "${TELEGRAM_DIR}/"
cp -R "${COMMON_DIR}/." "${SHORTCUT_DIR}/"

SOURCE_FILES=(
    awsclient.py
    apple_shortcut_handler.py
    env.py
    lambda_function.py
    telerobot_handler.py
)

for file in "${SOURCE_FILES[@]}"; do
    cp "${ROOT_DIR}/src/${file}" "${TELEGRAM_DIR}/${file}"
    cp "${ROOT_DIR}/src/${file}" "${SHORTCUT_DIR}/${file}"
done

sed -i.bak \
    's/from telerobot_handler import handler/from apple_shortcut_handler import handler/' \
    "${SHORTCUT_DIR}/lambda_function.py"
rm "${SHORTCUT_DIR}/lambda_function.py.bak"

find "${BUILD_DIR}" -type d -name __pycache__ -prune -exec rm -rf {} +
find "${BUILD_DIR}" -type f \( -name '*.pyc' -o -name '*.so' -o -name '*.dylib' \) -delete

rm -f \
    "${DIST_DIR}/telemage-telegram-python314.zip" \
    "${DIST_DIR}/telemage-shortcut-python314.zip"

(
    cd "${TELEGRAM_DIR}"
    zip -q -r "${DIST_DIR}/telemage-telegram-python314.zip" .
)

(
    cd "${SHORTCUT_DIR}"
    zip -q -r "${DIST_DIR}/telemage-shortcut-python314.zip" .
)

for archive in "${DIST_DIR}"/*.zip; do
    unzip -tq "${archive}" >/dev/null
    if unzip -l "${archive}" | grep -Eiq '(__pycache__|\.pyc$|\.so$|\.dylib$|darwin|cpython-31[0-3])'; then
        echo "Unexpected platform-specific file in ${archive}" >&2
        exit 1
    fi
done

echo "Created:"
echo "  ${DIST_DIR}/telemage-telegram-python314.zip"
echo "  ${DIST_DIR}/telemage-shortcut-python314.zip"
