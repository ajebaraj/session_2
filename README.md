# Flask Full-Stack Application

A modern full-stack web application built with Flask backend and vanilla HTML/CSS/JavaScript frontend.

## Features

### Frontend
- **Animal Selector**: Interactive radio buttons for cat, dog, and elephant with fade-in image animations
- **File Upload**: Drag-and-drop file upload with cloud icon and modern styling
- **Responsive Design**: Cards appear side-by-side on desktop, stacked on mobile
- **Modern UI**: Beautiful gradients, hover effects, and smooth animations

### Backend
- **Flask API**: Lightweight and fast web framework
- **File Upload Endpoint**: `/upload` endpoint that accepts POST requests
- **File Validation**: Checks file types and handles errors gracefully
- **Metadata Extraction**: Returns filename, size, and MIME type

## Project Structure

```
Session_2/
├── app.py                 # Flask backend server
├── templates/
│   └── index.html        # Frontend HTML/CSS/JS
├── static/
│   ├── styles.css        # Global stylesheet (theme + components)
│   └── images/           # Animal images (cat.jpg, dog.jpg, elephant.jpg)
├── uploads/              # Uploaded files storage
├── requirements.txt      # Flask dependencies
├── create_images.py      # Image generation script
├── start.sh             # Easy startup script
└── README.md            # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

**Option A: Using the startup script**
```bash
./start.sh
```

**Option B: Manual start**
```bash
python app.py
```

### 3. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

- `GET /` - Serves the main HTML page
- `POST /upload` - File upload endpoint
- `GET /uploads/<filename>` - Serve uploaded files

## File Upload API Response

When you upload a file, the API returns JSON with the following structure:

```json
{
    "filename": "example.txt",
    "size": "1.25 KB",
    "size_bytes": 1280,
    "type": "text/plain",
    "message": "File uploaded successfully!"
}
```

## Features in Detail

### Animal Selector (Box 1)
- Three radio buttons for cat, dog, and elephant
- Fade-in animation when selecting an animal
- Images are stored locally in `static/images/`
- Only one animal can be selected at a time

### File Upload (Box 2)
- Drag-and-drop file upload functionality
- Click to browse file option
- Cloud upload icon with modern styling
- Loading spinner during upload
- Success and error messages with animations
- Displays file metadata after successful upload:
  - Filename
  - File size (in B, KB, or MB)
  - MIME type

## Styling Features

- **Modern Design**: Gradient backgrounds, rounded corners, drop shadows
- **Hover Effects**: Cards lift on hover, buttons have smooth transitions
- **Animations**: Fade-in effects, slide-in animations, loading spinners
- **Responsive**: CSS Grid layout that adapts to screen size
- **Color Scheme**: Purple-blue gradient theme with white cards

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **File Handling**: Werkzeug for secure file uploads
- **Styling**: CSS Grid, Flexbox, CSS Animations

## Browser Compatibility

The application works on all modern browsers that support:
- ES6+ JavaScript features
- Fetch API
- CSS Grid and Flexbox
- File API and Drag & Drop

## Development

To run in development mode with auto-reload:

```bash
export FLASK_ENV=development
python app.py
```

## Customization

### Adding More Animals
1. Add new radio button in `templates/index.html`
2. Add corresponding image in `static/images/`
3. Update the JavaScript event handlers if needed

### Modifying Upload Behavior
- Edit the `/upload` endpoint in `app.py`
- Modify the upload logic in `templates/index.html`

### Styling Changes
- All styles are now in `static/styles.css`.
- The template links the stylesheet via `{{ url_for('static', filename='styles.css') }}`.
- Avoid inline styles; use classes defined in the stylesheet.

## Style Guide (UI-only)

### Theme tokens (CSS variables)
- Backgrounds: `--bg-light`, `--bg-dark`
- Text colors: `--text-light`, `--text-dark`
- Accent: `--accent` (gradient)

Usage: override in `:root` or add a `.light`/default dark scheme.

### Layout
- Container grid: `.dashboard` (2 columns, responsive to 1 column under 768px)
- Span full width: `.span-2`

### Components
- Card: `.card`
- Animal options row: `.animal-options`
- Animal option pill: `.animal-option` and state `.animal-option.active`
- Drop area: `.dropzone`
- Upload progress: `.bar > div`
- Preview image: `img.preview`
- History list: `.history-list` and `.history-list li`
- Toasts: `.toast-container`, `.toast`
- Theme toggle button: `.toggle-btn`

### States and accessibility
- Focus-visible styles inherit browser defaults; maintain sufficient contrast (AA).
- Keep interactive targets ≥ 40px height for touch.

### Do/Don’t
- Do reuse `.card` for any new sections.
- Do not rename element IDs or change form field names (preserves functionality).
- Do not add inline styles; extend the stylesheet instead.
