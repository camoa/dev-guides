---
description: Embed YouTube/Vimeo with the facade pattern, handle video autoplay policies, and implement background video with accessibility requirements
tldr: "Use the facade pattern for YouTube/Vimeo embeds on any performance-sensitive page — it saves ~500KB initial load. Use `<video autoplay muted loop playsinline>` for decorative background video."
---

# Video and Embed Craft

## When to Use

> Use the facade pattern for YouTube/Vimeo embeds on any performance-sensitive page — it saves ~500KB initial load. Use `<video autoplay muted loop playsinline>` for decorative background video. Use `<video controls>` for user-controlled content. Never use GIF for new animated content.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| YouTube/Vimeo embed, performance matters | Facade pattern or `lite-youtube-embed` | Saves ~500KB initial load; 3–5x better LCP |
| YouTube/Vimeo, simplicity over performance | Native iframe with `loading="lazy"` | Still defers load; worse than facade but better than eager |
| Decorative background video | `<video autoplay muted loop playsinline>` | Required for cross-browser mobile autoplay |
| User-controlled video | `<video controls poster="thumb.jpg">` | Accessibility-compliant |
| Replacing an animated GIF | `<video autoplay muted loop playsinline>` | 5–20x smaller; hardware-decoded |

## Pattern

**YouTube facade** (static thumbnail, swap iframe on click):
```html
<div class="video-facade" data-video-id="dQw4w9WgXcQ" style="aspect-ratio: 16/9;">
  <img src="https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    alt="Video: [Descriptive title]" loading="lazy" width="1280" height="720">
  <button class="play-btn" aria-label="Play video: [Descriptive title]">&#9654;</button>
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
Use `youtube-nocookie.com` to reduce tracking cookies.

**Background/decorative video** — all four attributes required:
```html
<video autoplay muted loop playsinline poster="video-poster.jpg">
  <source src="video.mp4" type="video/mp4">
</video>
```

**Reduced motion fallback for background video**:
```css
@media (prefers-reduced-motion: reduce) {
  .bg-video { display: none; }
  .bg-fallback { display: block; }
}
```

**Poster frame generation with FFmpeg**:
```bash
ffmpeg -i video.mp4 -ss 00:00:02 -frames:v 1 poster.jpg
```
Never use the first frame — it's often black. Pick a frame at 10–25% through the video.

**Autoplay policies**:

| Browser | Autoplay behavior |
|---|---|
| Chrome | Muted autoplay always allowed |
| Safari/iOS | Requires `muted` + `playsinline`; no autoplay in Low Power Mode |
| Firefox | Muted autoplay allowed |

**Background video file size budget**: < 3MB for a loop; aim < 1.5MB. Max 1080p; 720p often sufficient. Add WebM/VP9 alongside H.264 MP4 for 20–30% smaller files.

**Accessibility requirements**:
- Videos with speech/meaningful audio MUST have captions (`<track kind="captions">`)
- Decorative background video: `muted` required; add `aria-hidden="true"` on `<video>`
- Background videos running > 5 seconds need a user control to pause (WCAG 2.2.2)

## Common Mistakes

- **Wrong**: eager-loading YouTube iframes → **Right**: adds 500KB+ and multiple origin connections on load
- **Wrong**: `autoplay` without `muted` on mobile → **Right**: all mobile browsers block unmuted autoplay
- **Wrong**: missing `playsinline` on iOS → **Right**: video opens in fullscreen player, breaking layout
- **Wrong**: no `poster` attribute → **Right**: blank black frame shows while video buffers
- **Wrong**: background video without a pause control → **Right**: violates WCAG 2.2.2 (Pause, Stop, Hide)

## See Also

- [Image Format Strategy](image-format-strategy.md) — animated WebP vs `<video>` decision
- [Placeholder Strategies](placeholder-strategies.md) — poster images and aspect-ratio preservation
- Reference: [MDN Autoplay Guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)
- Reference: [web.dev Third-Party Embed Best Practices](https://web.dev/articles/embed-best-practices)
- Reference: [lite-youtube-embed](https://github.com/paulirish/lite-youtube-embed)
