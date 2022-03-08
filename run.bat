@echo off

set transform-script="%~dp0\transformAddresses\transformAddresses.py"

echo "Transforming addresses. This may take a minute..."

python3 %transform-script%

echo "Operation complete."

pause
