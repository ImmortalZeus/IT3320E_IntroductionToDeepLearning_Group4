@echo off
setlocal enabledelayedexpansion



REM Check if venv folder exists
if not exist venv (
    echo Virtual environment not found. Creating one...
    call python -m venv venv
)

call venv/Scripts/activate

where nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo NVIDIA driver not found.
    exit /b 1
)

REM Grab the line containing "CUDA Version"
for /f "delims=" %%L in ('nvidia-smi ^| findstr /i "CUDA Version"') do (
    set LINE=%%L
)

REM Extract the version number (last token)
for /f "tokens=9" %%A in ("!LINE!") do (
    set CUDA_VERSION=%%A
)

REM Trim spaces
for /f "tokens=* delims= " %%A in ("!CUDA_VERSION!") do (
    set CUDA_VERSION=%%A
)

echo Detected CUDA version: !CUDA_VERSION!

REM Split into major and minor parts
for /f "tokens=1 delims=." %%M in ("!CUDA_VERSION!") do (
    set MAJOR=%%M
)
for /f "tokens=2 delims=." %%N in ("!CUDA_VERSION!") do (
    set MINOR=%%N
)

set CUDA_CODE=!MAJOR!!MINOR!

echo CUDA code: !CUDA_CODE!

if "!CUDA_CODE!"=="118" (
    set TORCH_TAG=cu118
) else if "!CUDA_CODE!"=="119" (
    set TORCH_TAG=cu118
) else if "!CUDA_CODE!"=="120" (
    set TORCH_TAG=cu121
) else if "!CUDA_CODE!"=="121" (
    set TORCH_TAG=cu121
) else if "!CUDA_CODE!"=="122" (
    set TORCH_TAG=cu121
) else if "!CUDA_CODE!"=="123" (
    set TORCH_TAG=cu121
) else if "!CUDA_CODE!"=="124" (
    set TORCH_TAG=cu121
) else if "!CUDA_CODE!"=="127" (
    set TORCH_TAG=cu121
) else if "!CUDA_CODE!"=="128" (
    set TORCH_TAG=cu121
) else if "!CUDA_CODE!"=="129" (
    set TORCH_TAG=cu121
) else if "!CUDA_CODE!"=="130" (
    set TORCH_TAG=cu121
) else (
    set TORCH_TAG=cpu
)

call pip install pillow==10.2.0
call pip install requests==2.32.5
call pip install tqdm==4.67.1
call pip install numpy==1.26.4

if "!TORCH_TAG!"=="cpu" (
    echo Installing CPU-only PyTorch...
    call pip install "torch>=2.2.0,<2.3.0" "torchvision>=0.17.0,<0.18.0"
) else (
    echo Installing PyTorch for !TORCH_TAG!...
    call pip install "torch>=2.2.0,<2.3.0" "torchvision>=0.17.0,<0.18.0" --index-url https://download.pytorch.org/whl/!TORCH_TAG!
)
call pip install facenet_pytorch==2.6.0
call pip install flask==3.1.2
call pip install flask-cors==6.0.2
call pip install opencv-python==4.10.0.84
call pip install numpy==1.26.4

endlocal
