# mov.db

```
███╗   ███╗ ██████╗ ██╗   ██╗   ██████╗ ██████╗
████╗ ████║██╔═══██╗██║   ██║   ██╔══██╗██╔══██╗
██╔████╔██║██║   ██║██║   ██║   ██║  ██║██████╔╝
██║╚██╔╝██║██║   ██║╚██╗ ██╔╝   ██║  ██║██╔══██╗
██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ██╗██████╔╝██████╔╝
╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚═╝╚═════╝ ╚═════╝
```

<div align="center">

**A powerful command-line movie database manager powered by OMDB API**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)](https://www.sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OMDB](https://img.shields.io/badge/API-OMDB-red.svg)](http://www.omdbapi.com)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation)

</div>

---

## Overview

**mov.db** is a feature-rich CLI application for managing your personal movie database. Fetch movie data automatically from OMDB API, organize your collection, generate statistics, and create HTML landing pages for your movies.

### Why mov.db?

- **Fast & Lightweight** - Pure Python CLI with SQLite backend
- **Smart Search** - Automatic movie data fetching from OMDB API
- **Statistics** - Average ratings, median, best/worst movies at a glance
- **Random Picker** - Get random movie recommendations
- **Web Export** - Generate HTML landing pages with movie posters
- **Persistent Storage** - SQLite database for reliable data management

---

## Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| List Movies | View all movies with year and rating |
| Add Movie | Search and add movies via OMDB API |
| Delete Movie | Remove movies from your collection |
| Update Movie | Modify movie ratings |
| Statistics | Calculate average, median, best & worst ratings |
| Random Movie | Get a random movie recommendation |
| Search | Find movies by partial title match |
| Sort by Rating | View movies sorted by rating |
| Sort by Year | View movies sorted by release year |
| Generate Page | Create HTML landing page with posters |

### Technical Highlights

- **OMDB API Integration** - Automatic movie data fetching
- **SQLite Database** - Fast, reliable local storage
- **Dictionary-Based Returns** - Clean error handling without exception-based control flow
- **Separation of Concerns** - Storage layer independent from UI
- **PEP8 Compliant** - Professional Python code standards
- **Manual Sort Algorithms** - Educational implementation

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OMDB API Key ([Get one free here](http://www.omdbapi.com/apikey.aspx))

### Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/bastianwestholt/mov.db.git
cd mov.db
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment**
```bash
# Create .env file
echo "OMDB_API_KEY=your_api_key_here" > .env
```

**4. Run the application**
```bash
cd mov.db
python main.py
```

**Note:** Always run the application from the project directory.

### Dependencies

```txt
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0
```

---

## Usage

### Interactive Menu

```
********** My Movies Database *********

0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Movies sorted by year
10. Generate Landing-Page

Enter choice (0-10):
```

### Example Workflow

**Add a movie**
```
Enter choice: 2
Enter new movie name: Inception

Movie "Inception" (2010) added successfully with rating 8.8.
```

**View statistics**
```
Enter choice: 5

Average rating: 8.5
Median rating: 8.7
Best movie: Inception (2010), 8.8
Worst movie: The Room (2003), 3.6
```

**Search movies**
```
Enter choice: 7
Enter part of movie name: matrix

The Matrix (1999): 8.7
The Matrix Reloaded (2003): 7.2
```

**Generate HTML page**
```
Enter choice: 10

Landing page generated: _static/index.html
```

---

## Project Structure

```
mov.db/
├── main.py                  # Main CLI application
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
│
├── movie_storage/
│   ├── __init__.py
│   ├── movies_storage_sql.py    # SQLite storage layer
│   └── movies_storage.py        # Legacy JSON storage
│
├── data/
│   ├── movies.db                # SQLite database
│   ├── movies_dataset.json      # JSON data
│   └── movies_dataset_backup.json
│
└── _static/
    ├── index_template.html      # HTML template
    ├── style.css                # Stylesheet
    └── index.html               # Generated landing page
```

**Note:** Files like `.env`, `backups/`, `CLAUDE.md`, `REPORT.html`, `sanity_check.py`, and `movies_storage.py` are gitignored.

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
OMDB_API_KEY=your_omdb_api_key_here
```

### OMDB API

- **Free Tier:** 1,000 requests/day
- **Registration:** http://www.omdbapi.com/apikey.aspx
- **No credit card required**

---

## Documentation

### Storage Layer API

**`get_movies()`**
```python
Returns: dict - All movies as {title: {year, rating}}
```

**`add_movie(title)`**
```python
Args: title (str) - Movie title to search
Returns: dict - {"success": bool, "reason": str, ...}
```

**`delete_movie(title)`**
```python
Args: title (str) - Movie title to delete
Returns: bool - Success status
```

**`update_movie(title, rating)`**
```python
Args: title (str), rating (float) - New rating
Returns: bool - Success status
```

### Return Value Patterns

```python
# Success
{"success": True, "reason": "added", "title": "Inception", ...}

# Not found
{"success": False, "reason": "not_found", "title": "asdf"}

# Duplicate
{"success": False, "reason": "duplicate", "title": "Inception"}

# Database error
{"success": False, "reason": "database_error", "error": "..."}
```

---

## Code Philosophy

### Design Principles

1. **No Wrapper Functions** - Direct function references, no unnecessary abstraction
2. **Return Values over Exceptions** - Business logic uses return values, not exceptions
3. **Separation of Concerns** - Storage layer has no UI logic
4. **PEP8 Compliance** - Professional Python documentation standards
5. **Educational Focus** - Manual sort implementation for learning

### Architecture Pattern

```
┌─────────────────┐
│  Application    │  ← UI Logic, User Input, Formatting
│  Layer (CLI)    │
└────────┬────────┘
         │
┌────────▼────────┐
│  Storage Layer  │  ← Data Logic, OMDB API, SQLite
│  (SQL/JSON)     │
└─────────────────┘
```

---

## Known Issues

- **Median Calculation:** Uses middle index instead of average of two middle values for even counts
- **Update Function:** Asks for new rating even when rating was just fetched from OMDB
- **Poster Column:** Schema mismatch between table definition and INSERT statement

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP8 style guide
- Add docstrings to all functions
- No wrapper functions (KISS principle)
- Use return values instead of exceptions for business logic
- Keep storage layer free of UI logic

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **OMDB API** - For providing free movie data
- **SQLAlchemy** - Excellent Python SQL toolkit
- **MASTERSCHOOL** - Educational project foundation

---

## Contact

**Bastian Westholt**

- GitHub: [@bastianwestholt](https://github.com/bastianwestholt)
- Project: [mov.db](https://github.com/bastianwestholt/mov.db)

---

<div align="center">

**Made with care and code**

*Star this repository if you found it helpful*

</div>
