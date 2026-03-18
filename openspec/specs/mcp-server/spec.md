# Capability: MCP Server

Model Context Protocol server exposing backlog management tools — allows AI agents (Claude Code, Cursor, Copilot) to interact with the Bobr project programmatically.

## ADDED Requirements

### Requirement: read_backlog tool
The MCP server SHALL expose a `read_backlog` tool that lists backlog items with optional filters: `status`, `priority`, `item_type`, `epic`. It SHALL return a JSON array of item objects.

#### Scenario: Filter by status
- **WHEN** `read_backlog(status="open")` is called
- **THEN** only items with status=open SHALL be returned

#### Scenario: No filters
- **WHEN** `read_backlog()` is called without arguments
- **THEN** all backlog items SHALL be returned

---

### Requirement: get_ready_items tool
The MCP server SHALL expose a `get_ready_items` tool that returns items with status=open and no unresolved blocking dependencies, ordered by priority.

#### Scenario: Ready items
- **WHEN** `get_ready_items()` is called
- **THEN** only items that are open and unblocked SHALL be returned

---

### Requirement: claim_item tool
The MCP server SHALL expose a `claim_item` tool that atomically sets status=in-progress and assigns the item. Only items with status `open` or `in-review` SHALL be claimable. Default assignee SHALL be `mcp-agent`.

#### Scenario: Claim via MCP
- **WHEN** `claim_item(item_id="BL-a3f1")` is called on an open item
- **THEN** the item SHALL become in-progress with assignee=mcp-agent

#### Scenario: Claim non-claimable
- **WHEN** `claim_item(item_id="BL-a3f1")` is called on a done item
- **THEN** a ValueError SHALL be raised

---

### Requirement: FastMCP with JSON responses
The server SHALL use FastMCP with `json_response=True`, named "Bobr". It SHALL be runnable via `bobr mcp` entry point.

#### Scenario: Server startup
- **WHEN** `bobr mcp` is executed
- **THEN** the MCP server SHALL start and accept tool calls
