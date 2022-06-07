@echo off

@REM set transform-script="%~dp0\TransformAddresses.py"
set transform-script="TransformAddresses.py"
set data-directory="data/"
set data-prefix="address-import"
set export-directory="data/output"

echo "Transforming addresses. This may take a minute..."

python -m %transform-script% %data-directory% %data-prefix% %export-directory%

echo "Operation complete."

pause
