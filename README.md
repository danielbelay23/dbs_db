# Interactive Personal App

## 🌟 Features

- **Modern UI/UX**: Clean, responsive design with gradient background and card-based layout
- **Interactive Sections**:
  - About Me with personal interests and background
  - Skills categorization (Hard Skills & Soft Skills)
  - Detailed Work History with elegant card presentations
  - Projects & Accomplishments showcase
- **Downloadable Resume**: Option to download the full PDF resume
- **Responsive Design**: Adapts to different screen sizes
- **Custom Styling**: Professional color scheme with Montserrat and monospace fonts

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Styling**: Custom CSS, HTML
- **Data Visualization**: Plotly
- **Container Support**: Docker
- **Version Control**: Git with pre-commit hooks
- **Additional Libraries**: 
  - Pillow for image processing
  - pandas for data handling
  - streamlit-chat for interactive features

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip package manager
- Virtual environment

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/danielbelay23/dbs_db.git
cd digital_cv
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run about_daniel_belay.py
```

### 🐳 Docker Setup

1. Build the Docker image:
```bash
make docker_build
```

2. Run the container:
```bash
make docker_run
```

Or use docker-compose:
```bash
docker-compose up
```

## 📁 Project Structure

```
digital_cv/
├── assets/                 # Static assets (images, CSS)
├── src/                    # Source code
│   ├── text_utils.py      # Text processing utilities
│   └── data_utils.py      # Data handling utilities
├── pages/                  # Additional Streamlit pages
├── about_daniel_belay.py  # Main application file
├── requirements.txt       # Python dependencies
├── setup.sh              # Streamlit configuration
├── Makefile             # Build and run commands
└── docker-compose.yml   # Docker composition
```

## 🔧 Development

### Available Make Commands

- `make setup`: Install dependencies
- `make run`: Run app locally
- `make docker_build`: Build Docker image
- `make docker_run`: Run app in Docker container
- `make clean`: Clean up generated files

### Pre-commit Hooks

The project uses pre-commit hooks for code quality:
- YAML checking
- End of file fixing
- Trailing whitespace removal
- Black code formatting

## 📄 License

© 2025 Daniel Belay. All rights reserved.

## 🤝 Contributing

While this is a personal project, suggestions and feedback are welcome. Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Contact

- Email: danielkbelay2@gmail.com
- GitHub: [github.com/danielbelay23](https://github.com/danielbelay23)
