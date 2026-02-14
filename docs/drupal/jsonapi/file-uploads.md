---
description: "Uploading binary files (images, documents) to entity file/image fields. Separate operation from entity creation."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## File Uploads

### When to Use

Uploading binary files (images, documents) to entity file/image fields. Separate operation from entity creation.

### Steps

**1. Create or identify target entity:**
   - Entity must exist with file/image field

**2. Upload file:**
   - Method: `POST`
   - URL: `/jsonapi/{entity_type}/{bundle}/{uuid}/{field_name}`
   - Headers: `Accept: application/vnd.api+json`, `Content-Type: application/octet-stream`, `Content-Disposition: file; filename="name.ext"`, `Authorization`
   - Body: Binary file data

**3. Handle response:**
   - Success: `201 Created` with created file entity
   - Response includes file UUID and URI
   - File is automatically linked to entity field

### Pattern

**Upload image to article:**
```bash
curl -X POST "https://example.com/jsonapi/node/article/{uuid}/field_image" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/octet-stream" \
  -H "Content-Disposition: file; filename=\"photo.jpg\"" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  --data-binary @/path/to/photo.jpg
```

**Response:**
```json
{
  "data": {
    "type": "file--file",
    "id": "{file-uuid}",
    "attributes": {
      "uri": {
        "value": "public://2026-02/photo.jpg",
        "url": "/sites/default/files/2026-02/photo.jpg"
      },
      "filename": "photo.jpg",
      "filesize": 245816
    }
  }
}
```

**JavaScript with File input:**
```javascript
const fileInput = document.querySelector('input[type="file"]');
const file = fileInput.files[0];

fetch(`/jsonapi/node/article/${uuid}/field_image`, {
  method: 'POST',
  headers: {
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/octet-stream',
    'Content-Disposition': `file; filename="${file.name}"`,
    'Authorization': 'Basic ' + btoa('user:pass')
  },
  body: file
})
  .then(res => res.json())
  .then(data => console.log('Uploaded:', data.data.attributes.uri.url));
```

### Decision Points

| Field Type | Endpoint |
|------------|----------|
| Image field | `/jsonapi/node/article/{uuid}/field_image` |
| File field | `/jsonapi/node/article/{uuid}/field_document` |
| Media entity (image) | `/jsonapi/media/image/{uuid}/field_media_image` |

### Common Mistakes

**Using wrong Content-Type:** Must be `application/octet-stream` for binary uploads. WHY: Indicates raw binary data. Using `multipart/form-data` fails.

**Forgetting Content-Disposition header:** Filename must be specified. WHY: Drupal uses filename from header for stored file. Missing this causes default/ugly names.

**Uploading before creating entity:** File upload endpoint requires existing entity UUID. WHY: File must be attached to entity. Create entity first, then upload.

**Not validating file extensions:** Server validates against field configuration. WHY: Security and configuration. Uploading disallowed extensions returns 422 error.

**Uploading files larger than configured limit:** Check field max file size. WHY: Validation rejects oversized files. Also check PHP `upload_max_filesize` and `post_max_size`.

**Expecting automatic image style generation:** Original file is uploaded. WHY: Image styles are generated on-demand when accessed. Use image style URLs from field formatter.

### See Also
- [Creating Resources (POST)](creating-resources.md)
- [Updating Resources (PATCH)](updating-resources.md)
- [Code Reference Map](code-reference-map.md) (`src/Controller/FileUpload.php`)
