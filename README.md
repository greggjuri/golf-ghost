# Golf Ghost Analytics 🤖⛳

AI-Powered Golf Score Generation System with Sports Analytics Dashboard UI

## Overview

Golf Ghost Analytics generates realistic golf scores for a "ghost" player based on their GHIN handicap index. Perfect for practice rounds, simulations, or testing golf applications.

## Features

- **Smart Score Generation**: Uses GHIN handicap index, course rating, and slope to generate realistic scores
- **Modern Dark UI**: Sports analytics dashboard theme with color-coded scoring
- **Course Management**: Easy-to-use interface for adding and editing golf courses
- **Hole-by-Hole Input**: Individual fields for par, yardage, and handicap for each hole
- **Statistics Display**: Real-time gross score, net score, and course handicap calculations
- **Persistent Storage**: Courses saved to JSON for reuse

## Project Structure

```
golf-ghost/
├── main.py                 # Main application entry point
├── ghost_golfer.py         # Score generation logic
├── course_manager.py       # Course data management
├── ui_theme.py            # Dark analytics theme
├── ui_components.py       # Reusable UI widgets
├── generate_tab.py        # Generate round tab UI
├── manage_tab.py          # Manage courses tab UI
├── golf_courses.json      # Course database (auto-generated)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Installation

### Requirements

- Python 3.7+
- tkinter (usually comes with Python)

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd golf-ghost
```

2. Run the application:
```bash
python main.py
```

No additional dependencies required!

## Usage

### Generating a Ghost Round

1. Go to the **GENERATE ROUND** tab
2. Select a course from the dropdown
3. Enter the ghost player's GHIN handicap index
4. Click **GENERATE ROUND**
5. View the complete scorecard with color-coded scores:
   - 🟢 Green = Eagle or better
   - 🔵 Cyan = Birdie
   - ⚪ Gray = Par
   - 🟠 Orange = Bogey
   - 🔴 Red = Double bogey or worse

### Managing Courses

1. Go to the **MANAGE COURSES** tab
2. Click **NEW** or select an existing course to edit
3. Enter course details:
   - Course name
   - Tee name (Blue, White, Red, etc.)
   - Course rating
   - Slope rating
4. Enter hole-by-hole data:
   - Par for each hole
   - Yardage for each hole
   - Handicap index (1-18) for each hole
5. Click **SAVE COURSE**

### Pre-loaded Courses

The application comes with sample courses:
- Baytree National Golf Links (Blue Tees)
- Baytree National Golf Links (White Tees)

## How It Works

### Score Generation Algorithm

The ghost golfer generates realistic scores based on:

1. **Course Handicap Calculation**: 
   ```
   Course Handicap = (Handicap Index × Slope Rating) / 113
   ```

2. **Stroke Allocation**: Strokes are allocated to holes based on their handicap index

3. **Score Variation**: Random variation is added to simulate real play:
   - Overall round adjustment (gaussian distribution)
   - Per-hole randomness
   - Difficulty adjustments based on hole handicap

4. **Realistic Constraints**: Scores are bounded between eagle and triple bogey+

## File Descriptions

### Core Logic

- **ghost_golfer.py**: Contains the `GhostGolfer` class that handles score generation using handicap formulas and statistical distributions

- **course_manager.py**: Manages course data persistence, validation, and CRUD operations

### UI Components

- **ui_theme.py**: Defines the dark analytics theme colors and ttk styles

- **ui_components.py**: Reusable UI widgets (buttons, cards, headers, etc.)

- **generate_tab.py**: UI for the round generation tab with scorecard display

- **manage_tab.py**: UI for the course management tab with hole-by-hole inputs

- **main.py**: Application entry point and main window management

## Customization

### Changing the Theme

Edit `ui_theme.py` to customize colors:

```python
self.colors = {
    'bg_primary': '#0f172a',      # Main background
    'accent_blue': '#3b82f6',     # Primary accent
    'accent_green': '#10b981',    # Success/generate button
    # ... more colors
}
```

### Adjusting Score Algorithm

Modify `ghost_golfer.py` to change scoring behavior:

```python
# Adjust randomness
hole_randomness = random.gauss(0, 1.1)  # Change std deviation

# Adjust difficulty factors
if hole_hcp <= 6:
    difficulty_factor = 0.3  # Hard holes
```

## Technical Details

### Dependencies

- **tkinter**: GUI framework (built into Python)
- **json**: Course data storage
- **random**: Score generation randomness
- **os**: File system operations

### Data Format

Courses are stored in `golf_courses.json`:

```json
{
  "Course Name": {
    "tee_name": "Blue",
    "course_rating": 72.3,
    "slope_rating": 130,
    "par_values": [4, 4, 3, ...],
    "hole_handicaps": [7, 5, 15, ...],
    "yardages": [395, 405, 185, ...]
  }
}
```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - feel free to use this for any purpose.

## Future Enhancements

- [ ] Export scorecards to PDF
- [ ] Multiple ghost players in one round
- [ ] Historical score tracking
- [ ] Weather/wind conditions simulation
- [ ] Import courses from USGA database
- [ ] Stroke play vs match play modes
- [ ] Tournament mode with leaderboard

## Credits

Developed with Python and tkinter for golf enthusiasts and developers.

---

**Enjoy your ghost rounds! 🏌️‍♂️👻**
