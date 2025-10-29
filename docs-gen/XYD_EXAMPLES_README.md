# S2DM XYD Documentation Examples

This directory contains individual XYD documentation projects for each S2DM example, providing interactive GraphQL schema exploration.

## 🚀 Quick Start

### Start All Servers
```bash
./start-xyd-servers.sh
```

### Stop All Servers
```bash
./stop-xyd-servers.sh
```

## 📖 Available Examples

| Example | Port | URL | Hugo Page |
|---------|------|-----|-----------|
| Seat Capabilities | 5176 | [localhost:5176/api/seat-capabilities](http://localhost:5176/api/seat-capabilities) | [Hugo](http://localhost:61623/examples/seat-capabilities/example-documentation/) |
| Trailer Domain Model | 5177 | [localhost:5177/api/trailer-domain-model](http://localhost:5177/api/trailer-domain-model) | [Hugo](http://localhost:61623/examples/trailer-domain-model/example-documentation/) |
| Seat Domain Model | 5178 | [localhost:5178/api/seat-domain-model](http://localhost:5178/api/seat-domain-model) | [Hugo](http://localhost:61623/examples/seat-domain-model/example-documentation/) |
| Multiple Domains | 5179 | [localhost:5179/api/multiple-domains](http://localhost:5179/api/multiple-domains) | [Hugo](http://localhost:61623/examples/multiple-domains/example-documentation/) |
| Classification Schemes | 5180 | [localhost:5180/api/multiple-classification-schemes](http://localhost:5180/api/multiple-classification-schemes) | [Hugo](http://localhost:61623/examples/multiple-classification-schemes/example-documentation/) |
| Specification History | 5181 | [localhost:5181/api/specification-history-registry](http://localhost:5181/api/specification-history-registry) | [Hugo](http://localhost:61623/examples/specification-history-registry/example-documentation/) |

## 🏗️ Architecture

```
docs-gen/
├── xyd-examples/                    # Individual XYD projects
│   ├── seat-capabilities/           # Seat control operations
│   ├── trailer-domain-model/        # Trailer management system
│   ├── seat-domain-model/           # VSS-compliant seat hierarchy
│   ├── multiple-domains/            # Cross-domain patterns
│   ├── multiple-classification-schemes/ # SKOS classification
│   └── specification-history-registry/ # Version management
├── static/examples/                 # GraphQL schemas
├── content/examples/                # Hugo documentation pages
├── layouts/shortcodes/xyd-embed.html # XYD iframe shortcode
├── assets/css/xyd-embed.css        # Styling
└── assets/js/xyd-embed.js          # JavaScript enhancements
```

## 🔧 Individual Server Management

### Start Single Server
```bash
cd xyd-examples/seat-capabilities
xyd dev --port 5176
```

### Check Server Status
```bash
curl http://localhost:5176/api/seat-capabilities
```

### View Logs
```bash
tail -f /tmp/xyd-seat-capabilities.log
```

## 📝 Schema Management

### Update Schema
1. Edit schema in `static/examples/{example}/full_schema.graphql`
2. Copy to XYD project: `cp static/examples/{example}/full_schema.graphql xyd-examples/{example}/`
3. Restart XYD server

### Add New Example
1. Create directory: `mkdir xyd-examples/new-example`
2. Add `docs.json` configuration
3. Add GraphQL schema as `full_schema.graphql`
4. Create introduction page: `api/new-example/introduction.md`
5. Update startup script with new port
6. Add Hugo content page

## 🎨 Customization

### XYD Theme
Edit `docs.json` in each example to customize:
- Banner content
- Logo paths
- Navigation structure
- API routes

### Hugo Integration
Edit Hugo shortcode parameters:
- `src`: XYD server URL
- `height`: iframe height
- `title`: display title

Example:
```markdown
{{< xyd-embed src="http://localhost:5176/api/seat-capabilities" height="900px" title="Seat API" >}}
```

## 🚨 Troubleshooting

### Port Conflicts
- Change port in startup script
- Update Hugo shortcode src URL
- Restart affected servers

### Schema Errors
- Validate GraphQL syntax
- Check XYD logs: `/tmp/xyd-{example}.log`
- Verify schema file paths

### Missing Dependencies
```bash
cd xyd-examples/{example}
bun install  # or npm install
```

## 📦 Production Deployment

### Build Static Files
```bash
cd xyd-examples/{example}
xyd build
```

### Deploy to CDN
Static files generated in `.xyd/build/client/` can be deployed to any static hosting service.

### Update Hugo URLs
Replace localhost URLs with production URLs in Hugo shortcodes.
