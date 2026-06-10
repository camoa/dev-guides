---
description: AI operation types — chat, embeddings, text-to-image, and all 16 typed Input/Output classes
tldr: "16 operation types, each with typed Input/Output classes. Vision, audio, tools, and PDF are capabilities within chat — not separate types. 1.4.2 adds ChatWithPdf capability and ai.file_manager for provider-side document uploads."
drupal_version: "11.x"
---

# AI Operation Types

## When to Use

> Use this guide when calling a specific AI operation. Use [Provider System](provider-system.md) when you need to select or build providers.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Conversation or reasoning | `chat` / `ChatInterface` | Most common; supports streaming, tools, vision |
| Semantic vectors for RAG | `embeddings` / `EmbeddingsInterface` | Returns float array |
| Image generation | `text_to_image` / `TextToImageInterface` | Returns `ImageFile[]` |
| Content safety check | `moderation` / `ModerationInterface` | Returns scores per category |
| Audio transcription | `speech_to_text` / `SpeechToTextInterface` | Returns text |
| Need vision/tools/PDF | Capability filter on `chat` | Vision, tools, PDF are capabilities, not separate types |
| Upload doc, reference across turns | `ai.file_manager` + `ChatWithPdf` capability | Upload once, reference by remote ID |

## Operation Type Reference

| Type | Interface | Description |
|------|-----------|-------------|
| `chat` | `ChatInterface` | Conversations, reasoning |
| `embeddings` | `EmbeddingsInterface` | Vector embeddings for RAG |
| `text_to_image` | `TextToImageInterface` | Image generation |
| `image_to_image` | `ImageToImageInterface` | Image transformation |
| `image_to_video` | `ImageToVideoInterface` | Video from image |
| `text_to_speech` | `TextToSpeechInterface` | Audio generation |
| `speech_to_text` | `SpeechToTextInterface` | Transcription |
| `speech_to_speech` | `SpeechToSpeechInterface` | Audio-to-audio |
| `audio_to_audio` | `AudioToAudioInterface` | Audio transformation |
| `moderation` | `ModerationInterface` | Content safety |
| `image_classification` | `ImageClassificationInterface` | Image labeling |
| `object_detection` | `ObjectDetectionInterface` | Object detection |
| `rerank` | `RerankInterface` | Result reranking |
| `summarization` | `SummarizationInterface` | Text summarization |
| `translate_text` | `TranslateTextInterface` | Translation |
| `image_and_audio_to_video` | `ImageAndAudioToVideoInterface` | Video generation |

## Pattern

```php
use Drupal\ai\OperationType\Chat\ChatInput;
use Drupal\ai\OperationType\Chat\ChatMessage;

// Basic chat.
$messages = [
  new ChatMessage('system', 'You are a helpful assistant.'),
  new ChatMessage('user', 'Summarize this article.'),
];
$input = new ChatInput($messages);
$provider = \Drupal::service('ai.provider')->createInstance('anthropic');
$output = $provider->chat($input, 'claude-sonnet-4-20250514', ['my_module']);
$text = $output->getNormalized()->getText();

// Embeddings.
use Drupal\ai\OperationType\Embeddings\EmbeddingsInput;
$input = new EmbeddingsInput('Text to embed');
$output = $provider->embeddings($input, 'text-embedding-3-small', ['my_module']);
$vector = $output->getNormalized(); // float[]
```

## Chat with Tool Calling

```php
use Drupal\ai\OperationType\Chat\Tools\ToolsFunctionInput;
use Drupal\ai\OperationType\Chat\Tools\ToolsInput;

$tool = new ToolsFunctionInput('get_weather', [
  'name' => 'get_weather',
  'description' => 'Get weather for a location',
  'parameters' => [
    'type' => 'object',
    'properties' => ['location' => ['type' => 'string']],
    'required' => ['location'],
  ],
]);
$input->setTools(new ToolsInput([$tool]));
```

## Chat with PDF / Provider Files (New in 1.4.2)

Upload a document once to the provider's Files API, then reference it by remote ID across requests. Requires the provider to implement `AiFileProviderInterface` and the model to support the `ChatWithPdf` capability.

```php
use Drupal\ai\Entity\AiFileInterface;

// 1. Upload a local file to the provider (creates an ai_file entity).
$fileManager = \Drupal::service('ai.file_manager');
$aiFile = $fileManager->upload(
  '/path/to/report.pdf',
  owner_id: \Drupal::currentUser()->id(),
  provider_id: 'openai',
  purpose: AiFileInterface::PURPOSE_USER_DATA,
);

// 2. Reference the uploaded file by remote ID in a chat message.
$message = new ChatMessage('user', 'Summarize the attached report.');
$message->addRemoteFile($aiFile->getRemoteId());

$input = new ChatInput([$message]);
$output = $provider->chat($input, 'gpt-5.2', ['my_module']);
```

`AiFileManager` also provides `remoteDelete(AiFileInterface $file): bool` and `loadByPurpose(string $purpose, ?int $owner_id, int $limit): array`. Uploaded files are listed at `/admin/config/ai/files`.

**`ChatMessage` file methods:**
- `setFile(FileBaseInterface)` / `getFiles()` — any file type (inline)
- `setImage(ImageFile)` / `getImages()` — images only (kept for BC)
- `addRemoteFile($id)` / `getRemoteFiles()` / `removeRemoteFile($id)` — provider-side file references

## Structured Output

```php
$input = new ChatInput([new ChatMessage('user', 'Extract name and age from: John is 30.')]);
$input->setJsonSchema([
  'type' => 'object',
  'properties' => ['name' => ['type' => 'string'], 'age' => ['type' => 'integer']],
  'required' => ['name', 'age'],
]);
$data = json_decode($output->getNormalized()->getText(), TRUE);
```

## Capability Filter (Vision, Tools, PDF, etc.)

Vision, audio, tools, and PDF are **capabilities within `chat`**, not separate operation types. Filter for them using `AiModelCapability` enum values.

```php
use Drupal\ai\Enum\AiModelCapability;

// Get models that support vision.
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatWithImageVision]);

// Get models that support tool calling.
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatTools]);

// Get models that support PDF input.
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatWithPdf]);
```

| Capability | Value | Description |
|-----------|-------|-------------|
| `ChatWithImageVision` | `chat_with_image_vision` | Chat with image inputs |
| `ChatWithAudio` | `chat_with_audio` | Chat with audio inputs |
| `ChatWithPdf` | `chat_with_pdf` | **New in 1.4:** Chat with PDF document inputs |
| `ChatSystemRole` | `chat_system_role` | Supports system role |
| `ChatTools` | `chat_tools` | Native tool/function calling |
| `ChatStructuredResponse` | `chat_structured_response` | Native structured/schema responses |
| `ChatCombinedToolsAndStructuredResponse` | `chat_combined_tools_and_structured_response` | Tools + structured response in one call |

## Common Mistakes

- **Wrong**: Passing tags as empty array `[]` → **Right**: Always pass at least `['my_module']` — tags enable logging and guardrails
- **Wrong**: Not calling `setStreamedOutput(TRUE)` → **Right**: Streaming requires explicit opt-in
- **Wrong**: Searching for a `chat_with_image_vision` operation type → **Right**: Vision is a capability within `chat`, not a separate operation type
- **Wrong**: Not handling `StreamedChatMessageIteratorInterface` → **Right**: Streamed output returns an iterator, not a completed message
- **Wrong**: Inlining PDF bytes on every request → **Right**: Upload once via `ai.file_manager`, reference by remote ID

## See Also

- [Provider System](provider-system.md)
- [Enums and DTOs](enums-and-dtos.md)
- Reference: `web/modules/contrib/ai/src/OperationType/`
