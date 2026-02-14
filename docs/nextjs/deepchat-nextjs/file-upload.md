---
description: Configure file upload, handle FormData requests, and integrate with AI vision models for image analysis
---

# File Upload & Attachments

## When to Use

> Use `images` for image upload/analysis. Use `mixedFiles` for any file type (PDFs, docs). Always validate file types server-side.

## Decision

| Feature | Use Case |
|---------|----------|
| `images` | Image upload/analysis |
| `camera` | Web camera capture |
| `audio` | Audio file upload |
| `microphone` | Voice recording |
| `mixedFiles` | Any file type (PDFs, docs) |
| `dragAndDrop` | Better UX for files |

## Enable Image Upload

```tsx
<DeepChat
  images={true}
  connect={{
    url: '/api/chat',
    method: 'POST',
  }}
/>
```

## Custom File Configuration

```tsx
<DeepChat
  images={{
    files: {
      maxNumberOfFiles: 5,
      acceptedFormats: '.jpg,.png,.gif',
    },
    button: {
      position: 'inside-left',
    },
  }}
/>
```

## Mixed Files

```tsx
<DeepChat
  mixedFiles={{
    files: {
      maxNumberOfFiles: 3,
      acceptedFormats: '.pdf,.docx,.txt',
      infoModal: {
        textMarkDown: 'Upload up to 3 files (PDF, DOCX, TXT)',
      },
    },
  }}
/>
```

## Drag and Drop

```tsx
<DeepChat
  images={true}
  dragAndDrop={true}
/>
```

## Request Format

When files are uploaded, DeepChat sends `FormData` instead of JSON:

```
FormData {
  'message0': '{"role":"user","text":"Analyze this"}',
  'files': File { name: 'image.jpg', ... },
  'files': File { name: 'document.pdf', ... }
}
```

## API Route Handler

```typescript
export async function POST(request: NextRequest) {
  const contentType = request.headers.get('content-type');

  if (contentType?.includes('multipart/form-data')) {
    // File upload
    const formData = await request.formData();
    const files = formData.getAll('files') as File[];
    const message = JSON.parse(formData.get('message0') as string);

    // Process files
    const fileBuffers = await Promise.all(
      files.map(async (file) => ({
        name: file.name,
        type: file.type,
        buffer: Buffer.from(await file.arrayBuffer()),
      }))
    );

    // Send to AI provider with files
    const response = await processWithFiles(message.text, fileBuffers);
    return NextResponse.json({ html: response });
  } else {
    // Text-only message
    const body = await request.json();
    // ...
  }
}
```

## Image Analysis (OpenAI Vision)

```typescript
async function analyzeImage(text: string, imageBuffer: Buffer) {
  const base64Image = imageBuffer.toString('base64');

  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'gpt-4-vision-preview',
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text },
            {
              type: 'image_url',
              image_url: {
                url: `data:image/jpeg;base64,${base64Image}`,
              },
            },
          ],
        },
      ],
      max_tokens: 1000,
    }),
  });

  const data = await response.json();
  return data.choices[0].message.content;
}
```

## Pattern

```typescript
// Reusable file processor
async function processFiles(formData: FormData) {
  const files = formData.getAll('files') as File[];
  const message = JSON.parse(formData.get('message0') as string);

  const processedFiles = await Promise.all(
    files.map(async (file) => {
      const buffer = Buffer.from(await file.arrayBuffer());

      if (file.type.startsWith('image/')) {
        return { type: 'image', buffer, name: file.name };
      } else if (file.type === 'application/pdf') {
        return { type: 'pdf', buffer, name: file.name };
      } else {
        return { type: 'other', buffer, name: file.name };
      }
    })
  );

  return { message, files: processedFiles };
}
```

## Common Mistakes

- **Wrong**: Not checking `content-type` header → **Right**: Check for `multipart/form-data` before `request.formData()` to avoid parsing errors
- **Wrong**: Using `request.json()` on file upload → **Right**: Files are FormData, not JSON. This will throw an error
- **Wrong**: Not converting File to Buffer → **Right**: AI APIs expect base64 or binary. Use `arrayBuffer()` and Buffer
- **Wrong**: Forgetting to limit file size → **Right**: Set `maxNumberOfFiles` and validate size server-side
- **Wrong**: Not validating file types → **Right**: `acceptedFormats` is client-side only. Validate MIME type server-side
- **Wrong**: Sending large files to AI without compression → **Right**: Compress images before base64 encoding

## See Also

- [AI Provider Integration](ai-provider-integration.md)
- [Security](security.md)
- Reference: https://deepchat.dev/docs/files/
