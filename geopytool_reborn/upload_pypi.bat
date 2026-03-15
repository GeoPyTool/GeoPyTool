@echo off
REM GeoPyTool Reborn - Build and upload to PyPI
setlocal
cd /d "%~dp0"

if not defined PYTHON set "PYTHON=python"
set "VERSION_FILE=src\geopytool_reborn\__init__.py"

echo === GeoPyTool Reborn PyPI Upload ===

echo [1/5] Bumping patch version...
%PYTHON% -c "import re,sys;p='%VERSION_FILE%'.replace('\\','/');t=open(p).read();m=re.search(r'(__version__\s*=\s*\"(\d+\.\d+\.)(\d+)\")',t);old=m.group(2)+m.group(3);new=m.group(2)+str(int(m.group(3))+1);open(p,'w').write(t.replace(m.group(1),'__version__ = \"'+new+'\"'));print(f'  {old} -> {new}')"
if %errorlevel% neq 0 (echo Version bump failed! & exit /b 1)

echo [2/5] Cleaning old builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
if exist src\geopytool_reborn.egg-info rmdir /s /q src\geopytool_reborn.egg-info

echo [3/5] Installing build tools...
%PYTHON% -m pip install --upgrade build twine -q

echo [4/5] Building package...
%PYTHON% -m build
if %errorlevel% neq 0 (echo Build failed! & exit /b 1)
%PYTHON% -m twine check dist\*
if %errorlevel% neq 0 (echo Check failed! & exit /b 1)

echo [5/5] Uploading to PyPI...
%PYTHON% -m twine upload dist\*
if %errorlevel% neq 0 (echo Upload failed! & exit /b 1)

echo === Done! ===
endlocal