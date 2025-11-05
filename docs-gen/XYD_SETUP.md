# XYD Documentation Setup

This document describes the embedded XYD GraphQL documentation setup for S2DM examples.

## Overview

XYD (GraphQL documentation framework) is embedded into Hugo documentation pages for interactive GraphQL schema exploration with a built-in playground.

## Active Examples

Currently configured with XYD documentation for **two main examples**:

1. **Seat Domain Model** 
   - XYD Server: http://localhost:5176/api/seat-capabilities
   - Hugo Page: http://localhost:1313/examples/seat-domain-model/example-documentation/
   - Schema: Comprehensive seat domain with hierarchical components and capabilities
   
2. **Trailer Domain Model**
   - XYD Server: http://localhost:5177/api/trailer-domain-model
   - Hugo Page: http://localhost:1313/examples/trailer-domain-model/example-documentation/
   - Schema: Modular Vehicle → Trailer → Axle → Wheel hierarchy

## Architecture Notes

- The **seat-capabilities** XYD project serves the **seat-domain-model** documentation page
- This combines the seat capabilities schema with the domain model presentation
- Other examples (multiple-domains, classification-schemes, etc.) remain in the source but don't have XYD embeds

## Starting Servers

### Option 1: Use the startup script
```bash
cd /Users/q674786/s2dm/docs-gen
./start-xyd-servers.sh
```

### Option 2: Manual startup
```bash
# Terminal 1: Seat Capabilities
cd /Users/q674786/s2dm/docs-gen/xyd-examples/seat-capabilities
xyd dev --port 5176

# Terminal 2: Trailer Domain Model
cd /Users/q674786/s2dm/docs-gen/xyd-examples/trailer-domain-model
xyd dev --port 5177

# Terminal 3: Hugo Site
cd /Users/q674786/s2dm/docs-gen
npm run dev
```

## Stopping Servers

```bash
cd /Users/q674786/s2dm/docs-gen
./stop-xyd-servers.sh
```

Or manually:
```bash
pkill -f "xyd dev --port 517"
```

## Project Structure

```
docs-gen/
├── xyd-examples/                    # XYD project directories
│   ├── seat-capabilities/
│   │   ├── .xyd/                   # XYD framework installation
│   │   │   └── host/               # Dependencies (node_modules via bun)
│   │   ├── api/
│   │   │   └── seat-capabilities/
│   │   │       └── introduction.md
│   │   ├── docs.json               # XYD configuration
│   │   └── full_schema.graphql     # GraphQL schema
│   └── trailer-domain-model/
│       └── (same structure)
│
├── layouts/
│   └── shortcodes/
│       └── xyd-embed.html          # Hugo shortcode for embedding
│
├── assets/
│   ├── css/
│   │   └── xyd-embed.css          # Iframe styling
│   └── js/
│       └── xyd-embed.js           # Loading management
│
├── content/examples/
│   ├── seat-capabilities/
│   │   └── example-documentation.md  # Uses {{< xyd-embed >}}
│   └── trailer-domain-model/
│       └── example-documentation.md  # Uses {{< xyd-embed >}}
│
├── start-xyd-servers.sh            # Start XYD servers
└── stop-xyd-servers.sh             # Stop XYD servers
```

## XYD Configuration

Each XYD project has a `docs.json` configuration:

```json
{
  "theme": "picasso",
  "route": "api/example-name",
  "graphql": {
    "schemas": ["full_schema.graphql"]
  },
  "embedding": {
    "enabled": true,
    "allowOrigins": ["*"],
    "frameOptions": "ALLOWALL"
  }
}
```

## Hugo Embedding

Pages use the `xyd-embed` shortcode:

```markdown
---
layout: fullwidth
---

{{< xyd-embed 
  src="http://localhost:5176/api/seat-capabilities" 
  height="900px" 
  title="Seat Capabilities GraphQL API" 
>}}
```

## Troubleshooting

### XYD Server Won't Start

If you see "Cannot find package 'vite'" errors:

```bash
cd /Users/q674786/s2dm/docs-gen/xyd-examples/[example-name]/.xyd/host
bun install --frozen-lockfile
```

This uses bun's cache to install dependencies (works behind proxy/VPN).

### Network Issues

The setup is configured to work behind BMW's proxy:
- Proxy: `http://127.0.0.1:3128`
- VPN: Compatible
- Uses bun's package cache to avoid network downloads

### Port Conflicts

If ports 5176-5177 are in use:
```bash
lsof -i :5176 -i :5177
kill [PID]
```

## Logs

XYD server logs are saved to:
- `/tmp/xyd-seat-capabilities.log`
- `/tmp/xyd-trailer-domain-model.log`

View live logs:
```bash
tail -f /tmp/xyd-seat-capabilities.log
```

## Adding More Examples

To add XYD documentation for additional examples:

1. Create XYD project directory
2. Run `bun install --frozen-lockfile` in `.xyd/host/`
3. Update Hugo page with `{{< xyd-embed >}}`
4. Add to `start-xyd-servers.sh`

## Resources

- XYD Documentation: https://xyd.tools
- Hugo Shortcodes: https://gohugo.io/content-management/shortcodes/
- GraphQL Schema Documentation: In each example's schema file
