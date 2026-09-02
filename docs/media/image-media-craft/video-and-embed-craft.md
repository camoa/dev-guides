---
description: Embed YouTube/Vimeo with the facade pattern, handle video autoplay policies, and implement background video with accessibility requirements
tldr: "Use the facade pattern for YouTube/Vimeo embeds on any performance-sensitive page — it saves ~500KB initial load. Use `<video autoplay muted loop playsinline>` for decorative background video."
---

# Video and Embed Craft

## When to Use

> You need to embed third-party videos (YouTube, Vimeo), self-hosted video, or video-as-background. Each scenario has distinct performance implications and autoplay policy constraints.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| YouTube/Vimeo embed, performance matters | Facade pattern (`lite-youtube-embed` or custom) | Saves ~500KB initial load; 3–5x better LCP |
| YouTube/Vimeo, simplicity over performance | Native iframe with `loading="lazy"` | Still defers load; worse than facade but better than eager |
| Self-hosted video, decorative background | `<video autoplay muted loop playsinline>` | Required attributes for cross-browser mobile autoplay |
| Self-hosted video, user-controlled | `<video controls poster="thumb.jpg">` | Proper UX; accessibility-compliant |
| Replacing an animated GIF | `<video autoplay muted loop playsinline>` | 5–20x smaller; hardware-decoded |

## YouTube Facade Pattern

Load a static thumbnail image styled to look like the player. On click, swap in the real iframe.

```html
<div class="video-facade" data-video-id="dQw4w9WgXcQ" style="aspect-ratio: 16/9;">
  <img
    src="https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    alt="Video: [Descriptive title]"
    loading="lazy"
    width="1280"
    height="720"
  >
  <button class="play-btn" aria-label="Play video: [Descriptive title]">▶</button>
</div>
```
```js
document.querySelectorAll('.video-facade').forEach(facade => {
  facade.querySelector('.play-btn').addEventListener('click', () => {
    const id = facade.dataset.videoId;
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1`;
    iframe.allow = 'autoplay; encrypted-media; picture-in-picture';
    iframe.allowFullscreen = true;
    facade.replaceWith(iframe);
  });
});
```

Use `youtube-nocookie.com` to reduce tracking cookies. For a pre-built implementation, see [lite-youtube-embed](https://github.com/paulirish/lite-youtube-embed) (224x faster than native embed per Lighthouse tests).

## Video Autoplay Policies

| Browser | Autoplay behavior |
|---|---|
| Chrome | Muted autoplay always allowed; unmuted requires Media Engagement Index score |
| Safari/iOS | Requires `muted` + `playsinline`; will not autoplay in Low Power Mode or background tabs |
| Firefox | Muted autoplay allowed; site permissions can allow unmuted |

**The universal autoplay formula for background/decorative video:**
```html
<video autoplay muted loop playsinline poster="video-poster.jpg">
  <source src="video.mp4" type="video/mp4">
  <!-- Mobile fallback: static image if video unsupported -->
</video>
```

All four attributes are required: `autoplay` (starts video), `muted` (required for autoplay on mobile), `loop` (keeps playing), `playsinline` (prevents iOS fullscreen takeover).

## Poster Frame Selection

Never use the first frame as a poster — it is often a blank black frame or an unrepresentative composition. Select a frame at 10–25% through the video that shows the main subject clearly. Generate with FFmpeg:
```bash
ffmpeg -i video.mp4 -ss 00:00:02 -frames:v 1 poster.jpg
```

Poster image should follow the same format/optimization rules as regular images: WebP at 80% quality, explicit `width`/`height`.

## Video as Background — Performance

Background video is expensive. Mitigate with:
- **Max duration**: 6–15 seconds looping; longer means slower initial load
- **Resolution**: 1080p maximum; 720p often sufficient for backgrounds
- **Codec**: H.264 MP4 for broadest support; add WebM/VP9 for 20–30% smaller files on supporting browsers
- **Mobile fallback**: Detect `prefers-reduced-motion` and show a static image instead
- **File size budget**: < 3MB for a background video loop; aim for < 1.5MB

```css
@media (prefers-reduced-motion: reduce) {
  .bg-video { display: none; }
  .bg-fallback { display: block; }
}
```

## Accessibility

- **Captions**: All videos with speech or meaningful audio MUST have captions (`<track kind="captions">`)
- **Audio descriptions**: Videos where visual content conveys meaning not in audio need audio descriptions
- **Decorative background video**: Must be `muted`; should have `aria-hidden="true"` on the `<video>` element
- **Transcript**: Provide a linked transcript for longer informational videos
- **Play/pause control**: Background videos that run for more than 5 seconds need a user control to pause — WCAG 2.2 guideline 2.2.2

## Common Mistakes

- Eager-loading YouTube iframes — adds 500KB+ and multiple origin connections to initial page load
- Using `autoplay` without `muted` and expecting it to work on mobile — all mobile browsers block unmuted autoplay
- Missing `playsinline` on iOS — video opens in fullscreen player, breaking layout
- Not providing a `poster` — blank black frame shows while video buffers, looks broken
- Autoplaying video without a pause control — violates WCAG 2.2.2 (Pause, Stop, Hide)

## See Also

- [Image Format Strategy](image-format-strategy.md) — animated WebP vs `<video>` decision
- [Placeholder Strategies](placeholder-strategies.md) — poster images and aspect-ratio preservation
- Reference: [MDN Autoplay Guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)
- Reference: [web.dev Third-Party Embed Best Practices](https://web.dev/articles/embed-best-practices)
- Reference: [lite-youtube-embed](https://github.com/paulirish/lite-youtube-embed)
