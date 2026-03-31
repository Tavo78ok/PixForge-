 # 🖼 PixForge

> Advanced image processing tool for Linux — built with Python & Pillow

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Pillow](https://img.shields.io/badge/Pillow-10%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Linux-orange?logo=linux)
[![Build & Release](https://github.com/yourusername/pixforge/actions/workflows/build.yml/badge.svg)](https://github.com/yourusername/pixforge/actions)

PixForge is a full-featured image manipulation desktop application with a dark-themed GUI, covering everything Pillow can do — format conversion, transforms, color adjustments, filters, watermarking, batch processing, and more.

---

## ✨ Features

| Category | Capabilities |
|---|---|
| **Formats** | Open & save PNG, JPEG, BMP, GIF, TIFF, WebP, ICO, PPM/PGM/PBM |
| **Transform** | Resize (with aspect ratio lock), crop, rotate (free angle), flip H/V, transpose |
| **Adjustments** | Brightness, contrast, saturation, sharpness, color balance sliders |
| **Color ops** | Grayscale, invert, solarize, posterize, equalize, autocontrast |
| **Channels** | Extract R / G / B channels individually |
| **Filters** | 16+ filters: blur, sharpen, emboss, edge detect, Gaussian, unsharp mask… |
| **Drawing** | Text watermark with opacity, color border with picker |
| **Thumbnail** | Generate thumbnails at any max size |
| **Batch** | Convert entire folders between formats with one click |
| **History** | Undo / redo stack |
| **Canvas** | Zoom in/out/fit/1:1, mouse-wheel zoom, scroll |
| **Info panel** | Size, mode, format, EXIF note, grayscale range |

---

## 📦 Installation

### Option 1 — .deb package (Debian / Ubuntu / Mint)

```bash
# Download the latest release
wget https://github.com/yourusername/pixforge/releases/latest/download/pixforge_1.0.0_all.deb

# Install
sudo dpkg -i pixforge_1.0.0_all.deb
sudo apt-get install -f          # install any missing dependencies

# Launch
pixforge
```

### Option 2 — pip (any Linux with Python 3.10+)

```bash
pip install Pillow
python3 src/pixforge.py
```

### Option 3 — Run directly

```bash
git clone https://github.com/yourusername/pixforge.git
cd pixforge
pip install -r requirements.txt
python3 src/pixforge.py
```

---

## 🔧 Building the .deb yourself

```bash
git clone https://github.com/yourusername/pixforge.git
cd pixforge
chmod +x build_deb.sh
./build_deb.sh
# → pixforge_1.0.0_all.deb
```

Requirements: `dpkg-deb` (part of `dpkg` on any Debian system).

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Open image |
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+Q` | Quit |
| Mouse wheel | Zoom in/out |

---

## 📁 Project Structure

```
pixforge/
├── src/
│   └── pixforge.py           # Main application (single file)
├── debian/
│   ├── DEBIAN/
│   │   ├── control           # Package metadata
│   │   └── postinst          # Post-install script
│   └── usr/
│       ├── bin/pixforge       # Launcher
│       ├── share/
│       │   ├── applications/pixforge.desktop
│       │   ├── pixforge/      # App source installed here
│       │   └── doc/pixforge/copyright
├── .github/
│   └── workflows/build.yml   # CI/CD: build .deb + GitHub Release
├── build_deb.sh               # Local build script
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 🛠 Dependencies

- **Python 3.10+**
- **Pillow 10+** — image processing
- **Tkinter** — GUI (included with Python, may need `python3-tk` on some systems)

