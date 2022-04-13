@echo off

set transform-script="%~dp0\transformAddresses\transformAddresses.py"

echo "Transforming addresses. This may take a minute..."

python %transform-script%

echo "Operation complete."

pause
