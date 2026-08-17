---
description: Figma MCP Server — design-to-code AI workflows for Claude Code, VS Code, Cursor, and Windsurf
tracks: []
guide-meta:
  concepts:
    - Figma MCP
    - design-to-code
    - MCP tools
    - Code Connect
    - design tokens extraction
    - FigJam
    - selection workflow
    - link workflow
  not:
    - Figma plugin development
    - Figma REST API direct usage
  requires: []
  complements:
    - design-systems/recognition
    - design-systems/tailwind-tokens
    - design-systems/radix-sdc
  specializes: ""
  category: ai-tooling
---

# Figma MCP Server

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what the MCP server does and which type to use | [Figma MCP Overview](figma-mcp-overview.md) | When you want AI agents to generate code directly from Figma designs — using structured layout data, design tokens, and component mappings rather than screenshots alone. |
| Set up the remote server in Claude Code, VS Code, or Cursor | [Remote Server Setup](remote-server-setup.md) | Starting point for most developers. No Figma desktop app required. |
| Set up the desktop server with the Figma app | [Desktop Server Setup](desktop-server-setup.md) | When you want selection-based workflow: select frames in Figma, then prompt your agent to implement your current selection — no link copying needed. Requires Dev or Full seat on a paid Figma plan. |
| Use the Claude Code plugin shortcut | [Claude Code Plugin](claude-code-plugin.md) | When you want the fastest Claude Code setup — one command installs the server and pre-built skills for common Figma workflows. The plugin bundles the MCP server with curated skill definitions. |
| Look up all 13 available tools | [Available Tools Reference](available-tools-reference.md) | Look up a specific tool when you need to understand what it returns, when to trigger it explicitly, or what prompt phrasing activates it. Agents call most tools automatically — explicit triggers are for precision. |
| Extract design context for code generation | [Design Context Extraction](design-context-extraction.md) | Every code generation session starts here. `get_design_context` is the core tool — it converts Figma's visual representation into structured data AI agents can translate into code. |
| Get design tokens and variable values | [Design Tokens and Variables](design-tokens-and-variables.md) | When generating code that should reference design system tokens (colors, spacing, typography, border radius) by name rather than hardcoded values. Requires variables to be defined in Figma's Variables panel and applied to elements in the… |
| Link Figma components to my codebase | [Code Connect Integration](code-connect-integration.md) | When your codebase has existing component implementations you want AI agents to reuse rather than regenerate. Code Connect maps Figma components to actual code files, so generated code imports and uses your real components. |
| Get screenshots and metadata for large designs | [Screenshots and Metadata](screenshots-and-metadata.md) | Two complementary tools for handling cases where `get_design_context` alone is insufficient: screenshots provide visual ground truth; metadata provides structure without weight for large frames. |
| Generate or update FigJam diagrams | [FigJam and Diagram Tools](figjam-and-diagram-tools.md) | When your workflow involves FigJam diagrams — architecture maps, user flows, process diagrams — or when you want to generate new FigJam diagrams from code or descriptions. |
| Generate rules files for design system alignment | [Design System Rules](design-system-rules.md) | At the start of a project or after onboarding a new design system. `create_design_system_rules` generates a persistent rules file that tells your AI agent how to translate designs in your specific technology stack — component preferences,… |
| Choose between selection and link workflows | [Selection vs Link Workflows](selection-vs-link-workflows.md) | Every Figma MCP session requires choosing how to provide design context. This decision affects which server type you need and how fluid your workflow feels. |
| Write effective prompts for code generation | [Prompting Strategies](prompting-strategies.md) | When you want to get better code output from the MCP tools. Prompt specificity directly correlates with output quality — vague prompts produce generic React + Tailwind regardless of your stack. |
| Organize Figma files for better AI output | [Figma File Best Practices](figma-file-best-practices.md) | When preparing a Figma file for AI-assisted code generation. The quality of MCP output is directly proportional to how well the Figma file is structured. |
| Define custom agent rules for my project | [Custom Agent Rules](custom-agent-rules.md) | When you want consistent AI agent behavior across all Figma-to-code sessions in a project — same component imports, same token naming conventions, same file placement rules. Rules files persist between sessions and prevent agents from… |
| Understand rate limits and access tiers | [Rate Limits and Access Tiers](rate-limits-and-access-tiers.md) | Before committing to a workflow. Rate limits differ dramatically between plans — Starter plan users hit the monthly cap in a single session. |
| Review workflow patterns and anti-patterns | [Best Practices and Patterns](best-practices-and-patterns.md) | When setting up a sustainable design-to-code workflow. These practices apply across all clients and server types. |
| Understand limitations and workarounds | [Limitations and Workarounds](limitations-and-workarounds.md) | When you hit a wall — token limits, unexpected output, or workflow gaps. Understanding limitations prevents frustration and helps you find the right workaround. |
