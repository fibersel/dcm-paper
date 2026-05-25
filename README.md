# Comparative Analysis of AQM Algorithms: RED, ARED, Gentle RED

## Prerequisites

- Linux or macOS
- C++ compiler (g++ or clang++)
- CMake >= 3.16
- Python >= 3.8
- TeX Live (with LuaLaTeX and Biber)

## 1. Install ns-3

```bash
cd ~
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
git checkout ns-3.41
./ns3 configure --enable-examples --enable-tests
./ns3 build
```

## 2. Deploy simulation code

Copy the C++ source and configs into the ns-3 scratch directory:

```bash
mkdir -p ~/ns-3-dev/scratch/red-experiments/configs
cp code/*.cc code/*.h ~/ns-3-dev/scratch/red-experiments/
cp code/configs/*.txt ~/ns-3-dev/scratch/red-experiments/configs/
```

## 3. Run simulations

```bash
cd analysis
chmod +x run_simulations.sh
./run_simulations.sh
```

This runs RED, ARED, and Gentle RED simulations sequentially, moves CSV results to `analysis/`, and generates PGF figures in `image/`.

If you prefer to run manually:

```bash
cd ~/ns-3-dev
./ns3 run "scratch/red-experiments/red.cc --config=scratch/red-experiments/configs/red.txt"
./ns3 run "scratch/red-experiments/red.cc --config=scratch/red-experiments/configs/ared.txt"
./ns3 run "scratch/red-experiments/red.cc --config=scratch/red-experiments/configs/gentle.txt"
```

## 4. Generate figures

Install Python dependencies:

```bash
python -m venv ~/venv
source ~/venv/bin/activate
pip install pandas matplotlib
```

Run visualization:

```bash
cd analysis
python vis.py --algorithms red ared gentle --window 30
```

Output PGF files are written to `image/`.

## 5. Build the paper

```bash
make
```

Or manually:

```bash
lualatex default
biber default
lualatex default
lualatex default
```

The compiled PDF is placed in `out/default.pdf`.

## Directory structure

```
dcm-paper/
├── article.tex          # Paper content
├── default.tex          # Main driver file
├── definition.tex       # Preamble configuration
├── cite.bib             # Bibliography
├── Makefile             # Build automation
├── pfuproc.cls          # Document class
├── kproc.cls            # Base class
├── pfuproc/style/       # Journal style files
├── preamble/            # LaTeX preamble (fonts, packages)
├── image/               # Figures (PGF + logo)
├── code/                # ns-3 simulation source
│   ├── red.cc           # Main simulation
│   ├── config*.cc/h     # Configuration handling
│   ├── logging.cc/h     # Logging utilities
│   └── configs/         # AQM parameter files
├── analysis/            # Data processing
│   ├── vis.py           # Visualization script (PGF output)
│   └── run_simulations.sh
└── out/                 # Compiled PDF
```
