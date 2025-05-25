<p align="center">
  <a href="https://github.com/ValentinChanter/USAGI">
    <img src="https://i.imgur.com/UTxQu8i.png" height="96">
    <h3 align="center">USAGI</h3>
  </a>
</p>

<p align="center">UltraStar Automatic Groove Isolator</p>

<br/>

## Introduction

This app makes it easier to batch separate your UltraStar songs into instrumental and vocals using AI. \
This app was tested with Python 3.12.0, with a Nvidia GPU.

## Requirements

- [Python 3.10 or higher](https://www.python.org/downloads/)
- [FFmpeg](https://www.ffmpeg.org/download.html)

## Installation

Make sure requirements are installed before starting.

### Windows

.bat files are provided for easier installation. If you encounter any issue or you are using a different OS, please refer to [Manual installation](#manual-installation).

1. Clone this repo and access it

	```bash
	git clone https://github.com/ValentinChanter/USAGI
	cd USAGI
	```

2. Run setup.bat. It will create a python virtual environment in `venv` and install the required dependencies

	```bash
	setup.bat
	```

### Manual installation

1. Clone this repo and access it

	```bash
	git clone https://github.com/ValentinChanter/USAGI
	cd USAGI
	```

2. Create a virtual environment and activate it

	```bash
	python -m venv venv
	venv/Scripts/activate # Windows
    source venv/bin/activate # macOS or Unix 
	```

3. Update pip

	```bash
	pip install --upgrade pip
	```

4. Update setuptools and wheel

	```bash
	pip install --upgrade setuptools wheel
	```

5. Install dependencies depending on your hardware
   1. If you have a CUDA-capable GPU and will use it for faster processing

        ```bash
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
        pip install onnxruntime-gpu
        pip install -r requirements-gpu.txt
        ```

    2. If you don't have a CUDA-capable GPU and will use CPU for processing

        ```bash
        pip install -r requirements-cpu.txt
        ```

## Usage

1. Activate the previously created virtual environment and access the `src` folder

	```bash
	start.bat

    # or, if you cannot run start.bat

    venv/Scripts/activate # Windows
    source venv/bin/activate # macOS or Unix
    cd src
	```

2. Run the main python script.

	```bash
	python main.py [--force] path/to/ultrastar/songs/
	```

By default, [VOC] and [INSTR] are only generated if the song folder doesn't have any. Generation can be forced for all folders using `--force`. \
Files are considered audio if their extension is any of `mp3`, `wav`, `m4a` or `ogg`.
Specific folders can also be excluded by writing the exact folder name in the `src/exclusions.txt` file.