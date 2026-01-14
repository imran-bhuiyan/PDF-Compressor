# PDF-Compressor

A lightweight PDF compression utility for reducing PDF file sizes while preserving readable quality. This repository provides a command-line interface (CLI) and a Python library interface to compress PDF files in batch or from within applications.


## Features

- Compress PDF files to reduce storage and bandwidth usage
- Multiple quality/size presets (e.g., high, medium, low)
- CLI for batch processing
- Python API for programmatic use
- Optional integration with native tools (Ghostscript, qpdf) for improved compression (if available)

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [Python API](#python-api)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Development & Tests](#development--tests)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Quick Start

Clone the repository and install dependencies, then compress a PDF using the CLI:

```bash
git clone https://github.com/imran-bhuiyan/PDF-Compressor.git
cd PDF-Compressor
# install (adjust to your project's instructions)
pip install -e .
# example CLI usage (replace `pdf-compress` with the actual CLI command if different)
pdf-compress compress input.pdf output.pdf --quality medium
```

## Prerequisites

- Python 3.8+ (if this is a Python project)
- pip
- Optional: Ghostscript or qpdf for more aggressive compression (install via system package manager)

Install Ghostscript on Debian/Ubuntu:
```bash
sudo apt-get install ghostscript
```

Install qpdf on Debian/Ubuntu:
```bash
sudo apt-get install qpdf
```

## Installation

Install from PyPI (if published):
```bash
pip install pdf-compressor
```

Or install from source:
```bash
git clone https://github.com/imran-bhuiyan/PDF-Compressor.git
cd PDF-Compressor
pip install -r requirements.txt
pip install -e .
```

(If your project uses a different packaging or dependency method—poetry, pipenv, Docker—update these steps accordingly.)

## Usage

### CLI

Basic compression:
```bash
pdf-compress compress path/to/input.pdf path/to/output.pdf
```

With quality preset (example):
```bash
pdf-compress compress input.pdf output.pdf --quality low
```

Process a whole directory:
```bash
pdf-compress compress-dir --input-dir ./pdfs --output-dir ./compressed --quality medium
```

Show help for available options:
```bash
pdf-compress --help
pdf-compress compress --help
```

(Replace `pdf-compress` with your real CLI entrypoint name.)

### Python API

Example usage as a library:
```python
from pdf_compressor import compress_file, CompressionOptions

opts = CompressionOptions(quality="medium", use_ghostscript=True)
compress_file("input.pdf", "output.pdf", options=opts)
```

Or using an object-oriented API:
```python
from pdf_compressor import PDFCompressor

compressor = PDFCompressor(quality="low")
compressor.compress("input.pdf", "output.pdf")
```

Adjust import paths and class/function names to match the code in this repo.

## Configuration

- quality: high | medium | low — tradeoff between file size and visual fidelity
- use_ghostscript: true/false — whether to use Ghostscript if available
- output_path: path to write compressed file

Add a config file (optional)
```yaml
quality: medium
use_ghostscript: true
```

## Examples

Compress a single file (CLI):
```bash
pdf-compress compress invoice.pdf invoice_small.pdf --quality medium
```

Compress multiple files (Python):
```python
from pdf_compressor import batch_compress

files = ["a.pdf", "b.pdf", "c.pdf"]
batch_compress(files, "./out", quality="low")
```

## Troubleshooting

- Output file is larger than input:
  - Try a different quality preset.
  - Ensure external tools (Ghostscript/qpdf) are installed for better optimization.
- Corrupted output PDF:
  - Verify input is a valid PDF.
  - Try using a different compression backend or preset.
- Permission errors:
  - Check write permissions for the output directory.

## Development & Tests

Run tests:
```bash
# example using pytest
pytest
```

Linting:
```bash
# example using flake8 or black
flake8 .
black --check .
```

If the repo includes CI (GitHub Actions), check `.github/workflows` for the exact commands.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Run tests locally
5. Push to your fork: `git push origin feat/my-feature`
6. Open a Pull Request describing your changes

Please follow the repository's code style and include tests for new features or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. (Replace with the actual license if different.)

## Acknowledgements

- Ghostscript (if used)
- qpdf (if used)
- Inspired by various open-source PDF utilities

## Contact

Repository: [imran-bhuiyan/PDF-Compressor](https://github.com/imran-bhuiyan/PDF-Compressor)  
Author: imran-bhuiyan
