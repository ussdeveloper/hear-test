# 🎵 Professional Hearing Test Application

A modern, professional hearing test application with extended frequency range and comprehensive reporting capabilities.

## 🚀 Features

- **Extended Frequency Range**: 10Hz - 28kHz testing capability
- **Modern UI**: Flat design with intuitive controls
- **Real-time Visualization**: Interactive frequency scale with moving indicator
- **Comprehensive Testing**: Manual testing and quick frequency buttons
- **Professional Reports**: PDF generation with detailed analysis
- **Cross-platform Audio**: Pygame-based audio engine for reliability

## 📋 Requirements

- Python 3.8+
- Required packages (install with pip):
  ```bash
  pip install numpy pygame reportlab
  ```

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hearing-test
   ```

2. Create virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

Run the application:
```bash
python modern_hearing_test.py
```

### Testing Procedure:
1. **Adjust Frequency**: Use the slider (10Hz-28kHz) or quick test buttons
2. **Set Volume**: Adjust volume level as needed
3. **Play Tone**: Click "🎵 PLAY TONE" to start audio
4. **Record Response**: Click "✅ SŁYSZĘ" (Can Hear) or "🚫 NIE SŁYSZĘ" (Can't Hear)
5. **Generate Report**: Click "📊 GENERATE REPORT" for PDF analysis

## 🎛️ Interface Elements

- **Frequency Scale**: Visual representation with logarithmic scaling
- **Response Buttons**: Positioned on left (Can't Hear) and right (Can Hear) sides
- **Quick Test Frequencies**: Color-coded buttons for standard audiometric frequencies
- **Real-time Indicator**: Red marker shows current frequency position

## 📊 Report Generation

The application generates comprehensive PDF reports including:
- Test session summary
- Detailed frequency response data
- Success rate analysis
- Color-coded results table
- Basic hearing assessment recommendations

## 🎨 UI Features

- **Modern Design**: Flat buttons with hover effects
- **Color Coding**: Different colors for frequency ranges (Sub-Bass to Ultra-High)
- **Bilingual Support**: Polish and English labels
- **Professional Styling**: Uses Segoe UI font and consistent color scheme

## 🔧 Technical Details

- **Audio Engine**: Pygame mixer for cross-platform compatibility
- **Frequency Generation**: NumPy-based sine wave synthesis
- **UI Framework**: Tkinter with modern styling
- **PDF Reports**: ReportLab for professional document generation

## 📁 Project Structure

```
hearing-test/
├── modern_hearing_test.py    # Main application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
└── .venv/                   # Virtual environment (not in repo)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is for basic hearing screening purposes only. For comprehensive audiological assessment and medical advice, please consult a qualified audiologist or healthcare professional.

## 🎵 Audio Specifications

- **Sample Rate**: 44.1 kHz
- **Bit Depth**: 16-bit
- **Channels**: Stereo
- **Frequency Range**: 10Hz - 28kHz
- **Volume Control**: 0-100% with digital scaling
