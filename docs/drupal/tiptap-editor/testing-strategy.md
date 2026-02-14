---
description: You're building custom extensions or complex editor logic and need automated tests.
---

## 19.1 Testing Extensions & Editor Logic

### When to Use
You're building custom extensions or complex editor logic and need automated tests.

### Pattern
```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { Editor } from '@tiptap/core'
import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import CustomExtension from './CustomExtension'

describe('CustomExtension', () => {
  let editor: Editor

  beforeEach(() => {
    editor = new Editor({
      extensions: [Document, Paragraph, Text, CustomExtension],
      content: '<p>Initial content</p>',
    })
  })

  afterEach(() => {
    editor.destroy()
  })

  it('should register custom command', () => {
    expect(editor.commands.customCommand).toBeDefined()
  })

  it('should execute custom command', () => {
    const result = editor.commands.customCommand()
    expect(result).toBe(true)
  })

  it('should update content correctly', () => {
    editor.commands.setContent('<p>New content</p>')
    expect(editor.getHTML()).toBe('<p>New content</p>')
  })

  it('should detect active state', () => {
    editor.chain().selectAll().toggleBold().run()
    expect(editor.isActive('bold')).toBe(true)
  })

  it('should handle edge cases', () => {
    editor.commands.clearContent()
    expect(editor.isEmpty).toBe(true)
  })
})
```

### Integration Testing (React)
```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Editor from './Editor'

describe('Editor Component', () => {
  it('renders editor', () => {
    render(<Editor />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('allows typing', async () => {
    const user = userEvent.setup()
    render(<Editor />)

    const editor = screen.getByRole('textbox')
    await user.click(editor)
    await user.keyboard('Hello World')

    expect(editor).toHaveTextContent('Hello World')
  })

  it('executes toolbar commands', async () => {
    const user = userEvent.setup()
    render(<Editor />)

    await user.click(screen.getByRole('button', { name: /bold/i }))
    // Assert bold is active
  })
})
```

### E2E Testing (Playwright)
```typescript
import { test, expect } from '@playwright/test'

test('editor allows content editing', async ({ page }) => {
  await page.goto('/editor')

  const editor = page.locator('.tiptap')
  await editor.click()
  await editor.type('Hello World')

  await expect(editor).toHaveText('Hello World')
})

test('toolbar buttons work', async ({ page }) => {
  await page.goto('/editor')

  const editor = page.locator('.tiptap')
  await editor.click()
  await editor.type('Test')

  await page.click('button[aria-label="Bold"]')
  await expect(editor.locator('strong')).toHaveText('Test')
})
```

### Common Mistakes
- Not calling `editor.destroy()` in afterEach → Memory leaks in test suite
- Testing UI instead of logic → Test commands/state, not DOM rendering
- Not testing edge cases → Empty editor, long content, invalid input
- Forgetting async operations → Use `await` for commands that update state
- Not mocking external dependencies → Collaboration, API calls should be mocked

### See Also
- → 8.1 Custom Extension Architecture
- Reference: https://tiptap.dev/docs/editor/extensions/custom-extensions

