from flask import Flask, request, redirect, send_from_directory, render_template_string
import os
import uuid

app = Flask(__name__)

# Folder to save uploaded HTML files
SITES_FOLDER = 'sites'
os.makedirs(SITES_FOLDER, exist_ok=True)

# -------- Upload Page with original layout --------
UPLOAD_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nytrw Sites</title>
  <link rel="stylesheet" href="https://nytrw.github.io/nytrw-resc/static/styles.css">
  <style>
      .upload-button { padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 4px;}
  </style>
</head>
<body>
  <div class="top-section">
    <div class="left-side">
      <a href="https://nytrw.github.io/aboutus.html">About</a>
    </div>
    <div class="right-side">
      <a href="https://gmail.com/">Gmail</a>
      <a href="https://images.google.com/">Images</a>
      <img class="app-icon" src="https://cdn3.iconfinder.com/data/icons/feather-5/24/more-vertical-512.png" />
      <img class="profile-pic" src="https://nytrw.github.io/nytrw-resc/static/images/user_pic.png" />
    </div>
  </div>

  <div class="middle-section">
    <a href="index.html">
      <img class="search-logo-home" src="https://nytrw.github.io/nytrw-resc/static/images/logo.png" />
    </a>

    <!-- Upload Form -->
    <form id="upload-form" enctype="multipart/form-data" method="post" action="/upload">
      <br>
      <h1>Upload your site to Nytrw Sites</h1>
      <br>
      <input type="file" name="html_file" accept=".html" required />
      <br><br>
      <button type="submit" class="upload-button">Upload HTML</button>
    </form>
  </div>

  <div class="bottom-section">
    <div class="bottom-left">
      <a href="https://ads.google.com/">(fake) Advertising</a>
      <a href="https://smallbusiness.withgoogle.com/#!/">(fake) Business</a>
      <a href="https://www.google.com/search/howsearchworks/?fg=1">(fake) How Search works</a>
    </div>
    <div class="bottom-middle">
      <a href="https://sustainability.google/carbon-free/#home">(fake) Carbon Neutral since 2007</a>
    </div>
    <div class="bottom-right">
      <a href="https://policies.google.com/privacy?hl=en&fg=1">(fake) Privacy</a>
      <a href="https://policies.google.com/terms?hl=en&fg=1">(fake) Terms</a>
      <a href="https://www.google.com/settings">(fake) Settings</a>
    </div>
  </div>
</body>
</html>
"""

# -------- Success Page --------
SUCCESS_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nytrw Sites</title>
  <link rel="stylesheet" href="https://nytrw.github.io/nytrw-resc/static/styles.css">
  <style>
      .upload-button { padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 4px;}
  </style>
</head>
<body>
  <div class="top-section">
    <div class="left-side">
      <a href="https://nytrw.github.io/aboutus.html">About</a>
    </div>
    <div class="right-side">
      <a href="https://gmail.com/">Gmail</a>
      <a href="https://images.google.com/">Images</a>
      <img class="app-icon" src="https://cdn3.iconfinder.com/data/icons/feather-5/24/more-vertical-512.png" />
      <img class="profile-pic" src="https://nytrw.github.io/nytrw-resc/static/images/user_pic.png" />
    </div>
  </div>

  <div class="middle-section">
    <a href="index.html">
      <img class="search-logo-home" src="https://nytrw.github.io/nytrw-resc/static/images/logo.png" />
    </a>

    <!-- Upload Form -->
    <div class="middle-section" style="text-align: center; margin-top: 100px;">
        <h1>✅ Your HTML was successfully uploaded!</h1>
        <a href="{{ file_url }}" target="_blank" 
        style="color: #1a73e8; text-decoration: underline; font-size: 18px; display: inline-block; margin-top: 20px;">
        https://nytrw-api.onrender.com/{{ file_url }}
        </a>
    </div>

  <div class="bottom-section">
    <div class="bottom-left">
      <a href="https://ads.google.com/">(fake) Advertising</a>
      <a href="https://smallbusiness.withgoogle.com/#!/">(fake) Business</a>
      <a href="https://www.google.com/search/howsearchworks/?fg=1">(fake) How Search works</a>
    </div>
    <div class="bottom-middle">
      <a href="https://sustainability.google/carbon-free/#home">(fake) Carbon Neutral since 2007</a>
    </div>
    <div class="bottom-right">
      <a href="https://policies.google.com/privacy?hl=en&fg=1">(fake) Privacy</a>
      <a href="https://policies.google.com/terms?hl=en&fg=1">(fake) Terms</a>
      <a href="https://www.google.com/settings">(fake) Settings</a>
    </div>
  </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(UPLOAD_PAGE)

# -------- Handle Upload and redirect to success page --------
@app.route('/upload', methods=['POST'])
def upload_html():
    file = request.files.get('html_file')
    if not file or file.filename == '':
        return "No file selected", 400
    if not file.filename.endswith('.html'):
        return "Only HTML files are allowed", 400

    # Keep the original filename
    filename = file.filename
    file_path = os.path.join(SITES_FOLDER, filename)
    
    # Optional: avoid overwriting existing files
    if os.path.exists(file_path):
        return "A file with that name already exists", 400

    file.save(file_path)

    # Render success page with link to uploaded HTML
    file_url = f"/sites/{filename}"
    return render_template_string(SUCCESS_PAGE, file_url=file_url)


# -------- Serve uploaded HTML --------
@app.route('/sites/<path:filename>')
def serve_html(filename):
    file_path = os.path.join(SITES_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(SITES_FOLDER, filename)
    return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
