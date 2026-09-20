# MCP server configs

MCP (Model Context Protocol) servers give Claude access to tools and data outside
the chat — your filesystem, a database, an API.

## Two different files

| Client | File | Notes |
|---|---|---|
| Claude Code, project scope | `.mcp.json` in the repo root | Committed. Claude Code asks for approval before using it. |
| Claude Code, user scope | `~/.claude.json` | Available in all your projects. Easiest via the CLI. |
| Claude Desktop | `claude_desktop_config.json` | Restart the app after editing. |

Claude Desktop config location:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Easier than editing JSON

Claude Code can add servers for you:

```bash
claude mcp add --scope project filesystem -- npx -y @modelcontextprotocol/server-filesystem [ABSOLUTE_PATH]
claude mcp add --transport http [NAME] --scope project [URL]
claude mcp list
claude mcp reset-project-choices     # re-prompt for .mcp.json approvals
```

## A note on server packages

The official reference servers under `@modelcontextprotocol/` are a small, stable
set — filesystem, memory, sequential-thinking, fetch, git, time, everything.

Many first-party integrations have moved to the vendor's own package or to a hosted
HTTP endpoint rather than a local npm package. Before wiring up a service, check that
vendor's current MCP docs rather than assuming an `@modelcontextprotocol/server-*`
package still exists for it. `.mcp.http.json` shows the hosted form.

## The files here

| File | For |
|---|---|
| `.mcp.json` | Claude Code, project scope. Three local stdio servers. |
| `.mcp.http.json` | The hosted/HTTP form — a `url` instead of a `command`. |
| `claude_desktop_config.json` | Claude Desktop. **Restart the app after editing.** |

On Windows, paths inside JSON need **double** backslashes:
`"C:\\Users\\YourName\\Documents\\Project"`.

## Security

An MCP server runs with your permissions and can read whatever you point it at.
Scope the filesystem server to a specific directory — never your home folder or `/`.
Keep tokens in environment variables, not inline in a committed `.mcp.json`.
