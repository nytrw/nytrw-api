from flask import Flask, request, jsonify, send_from_directory, redirect
import os
import uuid

app = Flask(__name__)

# Folder to save HTML files
SITES_FOLDER = 'sites'
os.makedirs(SITES_FOLDER, exist_ok=True)

@app.route('/api', methods=['POST'])
def upload_html():
    data = request.json
    if not data or 'html' not in data:
        return jsonify({"error": "Missing 'html' in JSON body"}), 400

    html_content = data['html']
    # Generate a unique filename
    filename = f"{uuid.uuid4().hex}.html"
    file_path = os.path.join(SITES_FOLDER, filename)

    # Save the HTML content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Return the shortcut URL
    shortcut_url = f"/{filename}"
    return jsonify({"url": shortcut_url}), 201

# Route to serve the saved HTML files
@app.route('/sites/<path:filename>')
def serve_html(filename):
    return send_from_directory(SITES_FOLDER, filename)

# Catch-all route to redirect shortcut URLs to /sites/
@app.route('/<path:filename>')
def shortcut_redirect(filename):
    file_path = os.path.join(SITES_FOLDER, filename)
    if os.path.exists(file_path):
        return redirect(f"/sites/{filename}")
    return "File not found", 404

if __name__ == '__main__':
    # Disable debug/reloader to stop auto-restart
    app.run(host='0.0.0.0', port=5000, debug=False)
