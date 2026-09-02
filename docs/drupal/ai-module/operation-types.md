---
description: AI operation types — chat, embeddings, text-to-image, and all 16 typed Input/Output classes
tldr: "16 operation types, each with typed Input/Output classes. Vision, audio, tools, and PDF are capabilities within chat — not separate types. 1.4.2 adds ChatWithPdf capability and ai.file_manager for provider-side document uploads."
drupal_version: "11.x"
---

# AI Operation Types

## When to Use

> Use this guide when calling a specific AI operation. Use [Provider System](provider-system.md) when you need to select or build providers.

The AI module supports 15 operation types. Each has typed Input/Output classes in `src/OperationType/{Type}/`.

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

| Type | Interface | Input Class | Output Class | Description |
|------|-----------|-------------|--------------|-------------|
| `chat` | `ChatInterface` | `ChatInput` | `ChatOutput` | Conversations, reasoning |
| `embeddings` | `EmbeddingsInterface` | `EmbeddingsInput` | `EmbeddingsOutput` | Vector embeddings for RAG |
| `text_to_image` | `TextToImageInterface` | `TextToImageInput` | `TextToImageOutput` | Image generation |
| `image_to_image` | `ImageToImageInterface` | `ImageToImageInput` | `ImageToImageOutput` | Image transformation |
| `image_to_video` | `ImageToVideoInterface` | `ImageToVideoInput` | `ImageToVideoOutput` | Video from image |
| `text_to_speech` | `TextToSpeechInterface` | `TextToSpeechInput` | `TextToSpeechOutput` | Audio generation |
| `speech_to_text` | `SpeechToTextInterface` | `SpeechToTextInput` | `SpeechToTextOutput` | Transcription |
| `speech_to_speech` | `SpeechToSpeechInterface` | `SpeechToSpeechInput` | `SpeechToSpeechOutput` | Audio-to-audio |
| `audio_to_audio` | `AudioToAudioInterface` | `AudioToAudioInput` | `AudioToAudioOutput` | Audio transformation |
| `moderation` | `ModerationInterface` | `ModerationInput` | `ModerationOutput` | Content safety |
| `image_classification` | `ImageClassificationInterface` | `ImageClassificationInput` | `ImageClassificationOutput` | Image labeling |
| `object_detection` | `ObjectDetectionInterface` | `ObjectDetectionInput` | `ObjectDetectionOutput` | Object detection |
| `rerank` | `RerankInterface` | `RerankInput` | `RerankOutput` | Result reranking |
| `summarization` | `SummarizationInterface` | `SummarizationInput` | `SummarizationOutput` | Text summarization |
| `translate_text` | `TranslateTextInterface` | `TranslateTextInput` | `TranslateTextOutput` | Translation |
| `image_and_audio_to_video` | `ImageAndAudioToVideoInterface` | `ImageAndAudioToVideoInput` | `ImageAndAudioToVideoOutput` | Video generation |

## Chat (Most Common)

```php
use Drupal\ai\OperationType\Chat\ChatInput;
use Drupal\ai\OperationType\Chat\ChatMessage;

$messages = [
  new ChatMessage('system', 'You are a helpful assistant.'),
  new ChatMessage('user', 'Summarize this article.'),
];
$input = new ChatInput($messages);

// Optional: enable streaming
$input->setStreamedOutput(TRUE);

// Optional: set configuration
$input->setModelConfiguration(['temperature' => 0.7, 'max_tokens' => 1024]);

// Execute
$provider = \Drupal::service('ai.provider')->createInstance('anthropic');
$output = $provider->chat($input, 'claude-sonnet-4-20250514', ['my_module']);

// Get response
$normalized = $output->getNormalized(); // ChatMessage
$text = $normalized->getText();
$role = $normalized->getRole(); // 'assistant'
```

## Chat with Tool Calling

```php
use Drupal\ai\OperationType\Chat\Tools\ToolsInput;
use Drupal\ai\OperationType\Chat\Tools\ToolsFunctionInput;
use Drupal\ai\OperationType\Chat\Tools\ToolsPropertyInput;

$tool = new ToolsFunctionInput('get_weather', [
  'name' => 'get_weather',
  'description' => 'Get weather for a location',
  'parameters' => [
    'type' => 'object',
    'properties' => [
      'location' => ['type' => 'string', 'description' => 'City name'],
    ],
    'required' => ['location'],
  ],
]);
$toolsInput = new ToolsInput([$tool]);
$input->setTools($toolsInput);
```

## Chat with Images (Vision)

```php
use Drupal\ai\OperationType\GenericType\ImageFile;

$image = new ImageFile(file_get_contents('/path/to/image.jpg'), 'image/jpeg', 'photo.jpg');
$message = new ChatMessage('user', 'Describe this image.');
$message->setImage($image);
// Or load straight from a Drupal file entity: $message->setImageFromFile($fileEntity);
```

## Chat with PDF / Provider Files (New in 1.4.2)

Large documents (PDFs, datasets) can be uploaded once to a provider's Files API and then referenced by remote ID in chat messages — instead of inlining the bytes on every request. The `ai.file_manager` service (`AiFileManager`) handles the lifecycle; the provider must implement `AiFileProviderInterface` (see [Provider System](provider-system.md)) and the model should advertise the `ChatWithPdf` capability.

```php
use Drupal\ai\Entity\AiFileInterface;

// 1. Upload a local file to the provider (creates an `ai_file` entity).
$fileManager = \Drupal::service('ai.file_manager');
$aiFile = $fileManager->upload(
  '/path/to/report.pdf',                 // local path OR a FileBaseInterface
  owner_id: \Drupal::currentUser()->id(),
  provider_id: 'openai',
  metadata: ['expires_after' => 3600],   // optional, provider-specific
  purpose: AiFileInterface::PURPOSE_USER_DATA,
);

// 2. Reference the uploaded file by its remote ID in a chat turn.
$message = new ChatMessage('user', 'Summarize the attached report.');
$message->addRemoteFile($aiFile->getRemoteId());

$input = new ChatInput([$message]);
$output = $provider->chat($input, 'gpt-5.2', ['my_module']);
```

`AiFileManager` also provides `remoteDelete(AiFileInterface $file): bool` and `loadByPurpose(string $purpose, ?int $owner_id = NULL, int $limit = 50): array`. On failure to save the entity after a successful remote upload, `upload()` rolls back the remote file automatically. Uploaded files are `ai_file` content entities listed at `/admin/config/ai/files`. Declared **purposes** (`AiFileInterface::PURPOSE_*`): `assistants`, `batch`, `fine-tune`, `vision`, `user_data` (default), `evals`, `rag_storage`, `ocr`.

> **`ChatMessage` file methods:** `setFile(FileBaseInterface)` / `getFiles()` (any file type), `setImage(ImageFile)` / `getImages()` (images only — kept for BC), and `addRemoteFile($id)` / `getRemoteFiles()` / `removeRemoteFile($id)` for provider-side file references.

## Embeddings

```php
use Drupal\ai\OperationType\Embeddings\EmbeddingsInput;

$input = new EmbeddingsInput('Text to embed');
$output = $provider->embeddings($input, 'text-embedding-3-small', ['my_module']);
$vector = $output->getNormalized(); // float[]
```

## Text to Image

```php
use Drupal\ai\OperationType\TextToImage\TextToImageInput;

$input = new TextToImageInput('A cat wearing a space helmet');
$output = $provider->textToImage($input, 'dall-e-3', ['my_module']);
$images = $output->getNormalized(); // ImageFile[]
$binary = $images[0]->getBinary();
$mime = $images[0]->getMimeType();
```

## Structured Output (JSON Schema)

```php
$input = new ChatInput([new ChatMessage('user', 'Extract name and age from: John is 30.')]);
$input->setJsonSchema([
  'type' => 'object',
  'properties' => [
    'name' => ['type' => 'string'],
    'age' => ['type' => 'integer'],
  ],
  'required' => ['name', 'age'],
]);
$output = $provider->chat($input, $model, ['extraction']);
$data = json_decode($output->getNormalized()->getText(), TRUE);
```

## Capability-Based Pseudo Operation Types

Some operations are **not** separate operation types but rather **capabilities** within the `chat` type. Filter for them using `AiModelCapability` enum values in `getConfiguredModels()`:

| Capability Enum | Filter Value | Description |
|----------------|-------------|-------------|
| `ChatWithImageVision` | `chat_with_image_vision` | Chat with image inputs (vision) |
| `ChatWithAudio` | `chat_with_audio` | Chat with audio inputs |
| `ChatWithVideo` | `chat_with_video` | Chat with video inputs |
| `ChatWithPdf` | `chat_with_pdf` | **New in 1.4:** Chat with PDF document inputs |
| `ChatSystemRole` | `chat_system_role` | Supports system role in messages |
| `ChatJsonOutput` | `chat_json_output` | Reliable complex JSON output |
| `ChatStructuredResponse` | `chat_structured_response` | Native structured/schema responses |
| `ChatTools` | `chat_tools` | Native tool/function calling |
| `ChatCombinedToolsAndStructuredResponse` | `chat_combined_tools_and_structured_response` | Both tools and structured response in one request |

```php
// Get models that support vision
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatWithImageVision]);

// Get models that support tool calling
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatTools]);

// Get models that support PDF input
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatWithPdf]);
```

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Not passing tags | Breaks logging, guardrails, and event filtering |
| Forgetting `setStreamedOutput(TRUE)` for streaming | Non-streamed by default; streaming requires explicit opt-in |
| Not handling `StreamedChatMessageIteratorInterface` | Streamed output returns an iterator, not a completed message |
| Searching for a "chat_with_image_vision" operation type | Vision is a capability within `chat`, not a separate operation type |
| Inlining PDF bytes on every request | Upload once via `ai.file_manager` and reference by remote ID |

## See Also

- [Provider System](provider-system.md)
- [Enums and DTOs](enums-and-dtos.md)
- Reference: `web/modules/contrib/ai/src/OperationType/`
