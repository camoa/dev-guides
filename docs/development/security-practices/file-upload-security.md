---
description: Secure file upload handling including magic byte validation, secure storage, malware scanning, filename sanitization, and path traversal prevention.
---

# File Upload Security

## When to Use

Any feature that accepts files from users — profile pictures, document uploads, file sharing, import features, email attachments. File uploads are extremely dangerous: remote code execution, stored XSS, DoS, malware distribution.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Validate file type | **Magic byte inspection** + extension allowlist | MIME type spoofing is trivial |
| Store uploaded files | Outside web root + randomized names | Prevents direct execution, path traversal |
| Scan for malware | Antivirus API (ClamAV, VirusTotal) | Detect malicious files |
| Limit file size | Server config + application check | Prevent DoS via disk exhaustion |
| Serve uploaded files | Separate domain or CDN | Isolate from application domain |
| Validate images | Re-encode with image library | Strip metadata, prevent polyglots |

## File Type Validation

**NEVER trust client-provided MIME type:**

```python
# Bad: Trust Content-Type header
if file.content_type == 'image/jpeg':  # Attacker controls this!
    file.save(f'uploads/{file.filename}')
# Attacker sends shell.php with Content-Type: image/jpeg → Remote code execution
```

**Good: Validate with magic bytes:**

```python
import magic

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
ALLOWED_MIME_TYPES = {
    'image/png': [b'\x89PNG'],
    'image/jpeg': [b'\xff\xd8\xff'],
    'image/gif': [b'GIF87a', b'GIF89a'],
    'application/pdf': [b'%PDF-']
}

def validate_file(file):
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f'Extension .{ext} not allowed')

    file_data = file.read(8192)
    file.seek(0)
    mime_type = magic.from_buffer(file_data, mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f'MIME type {mime_type} not allowed')

    if mime_type.startswith('image/'):
        validate_image(file)
    return filename, mime_type

def validate_image(file):
    from PIL import Image
    img = Image.open(file)
    img.verify()
    file.seek(0)
    # Re-encode to strip metadata and malicious content
    img = Image.open(file)
    output = io.BytesIO()
    img.save(output, format=img.format)
    return output.getvalue()
```

## Secure File Storage

```python
UPLOAD_DIR = '/var/app/uploads'  # OUTSIDE web root
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['upload']

    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return {"error": "File too large"}, 413

    filename, mime_type = validate_file(file)

    # Generate unpredictable filename
    safe_filename = f"{uuid.uuid4()}.{filename.rsplit('.', 1)[1]}"

    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    # Ensure path is within UPLOAD_DIR (prevent ../ traversal)
    real_path = os.path.realpath(file_path)
    if not real_path.startswith(os.path.realpath(UPLOAD_DIR)):
        return {"error": "Invalid path"}, 400

    file.save(file_path)
    return {"id": safe_filename.split('.')[0]}, 200
```

## Serving Uploaded Files

```python
@app.route('/uploads/<uuid:file_id>')
def serve_upload(file_id):
    file_record = db.execute("SELECT * FROM uploads WHERE uuid = ?", [str(file_id)]).fetchone()
    if not file_record:
        return {"error": "Not found"}, 404
    if file_record['user_id'] != current_user.id and not current_user.is_admin:
        return {"error": "Forbidden"}, 403
    return send_file(
        file_path,
        mimetype=file_record['mime_type'],
        as_attachment=True,  # Force download, don't display inline
        download_name=file_record['original_filename']
    )
```

**Serve from separate domain (best practice):** Use `uploads.example.com`, not `www.example.com`. Prevents XSS on main domain if malicious file is uploaded.

## Malware Scanning

```python
import pyclamd

clamd = pyclamd.ClamdUnixSocket()

def scan_file(file_path):
    result = clamd.scan_file(file_path)
    if result is None:
        return True  # No virus found
    virus_name = result[file_path][1]
    return False, virus_name
```

## Path Traversal Prevention

```python
# Bad: Vulnerable to path traversal
@app.route('/download/<filename>')
def download_bad(filename):
    file_path = os.path.join('/var/uploads', filename)
    return send_file(file_path)  # ../../etc/passwd

# Good: Validate path
@app.route('/download/<filename>')
def download_safe(filename):
    safe_filename = secure_filename(filename)
    file_path = os.path.join('/var/uploads', safe_filename)
    real_path = os.path.realpath(file_path)
    real_upload_dir = os.path.realpath('/var/uploads')
    if not real_path.startswith(real_upload_dir):
        return {"error": "Invalid path"}, 400
    return send_file(real_path)
```

## Image-Specific Security

```python
from PIL import Image

def sanitize_image(file):
    """Strip EXIF metadata and re-encode"""
    img = Image.open(file)
    data = list(img.getdata())
    image_without_exif = Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    output = io.BytesIO()
    image_without_exif.save(output, format='PNG')
    return output.getvalue()

# SVG uploads are EXTREMELY dangerous
# SVG can contain JavaScript, external resources
# Option 1: Don't allow SVG uploads (safest)
# Option 2: Sanitize with dedicated library (lxml + defusedxml)
```

## Common Mistakes

- **Trusting Content-Type header** — Attacker fully controls this. Validate magic bytes, not headers
- **Storing files in web root** — `/var/www/html/uploads/shell.php` is accessible and executable
- **Not randomizing filenames** — User uploads `shell.php`, visits `/uploads/shell.php`, code executes
- **No file size limits** — Attacker uploads 10GB file repeatedly. Disk fills, DoS
- **Serving files inline** — `Content-Disposition: inline` displays HTML/JS files in browser. Use `attachment`
- **Allowing .htaccess uploads** — User uploads `.htaccess` to enable PHP execution. Block dotfiles
- **Double extension bypass** — `shell.php.jpg` — some servers execute as PHP
- **Not scanning for malware** — User uploads ransomware, another user downloads it
- **SVG uploads without sanitization** — SVG can contain `<script>` tags

## See Also

- Previous: [API Security](api-security.md) | Next: [Dependency Security](dependency-security.md)
- Reference: [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- Reference: [Unrestricted File Upload - OWASP](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
