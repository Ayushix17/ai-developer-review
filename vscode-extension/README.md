# VS Code Extension - AI Code Reviewer

Real-time AI-powered code analysis, suggestions, and improvements directly in VS Code.

## Phase 7: VS Code Extension

Integrates with the FastAPI backend to provide:
- ✅ Code analysis and suggestions
- ✅ Code improvement recommendations
- ✅ Code explanation
- ✅ Inline diagnostics
- ✅ GitHub integration

## 🚀 Setup

### Prerequisites
- Node.js 16+
- VS Code 1.80+
- Backend API running (`http://localhost:8000`)

### Installation

```bash
cd vscode-extension

# Install dependencies
npm install

# Build extension
npm run compile

# Debug in VS Code
# Press F5 to launch extension in debug mode
```

## 📦 Commands

| Command | Keybinding | Description |
|---------|-----------|-------------|
| Analyze Code | `Ctrl+Shift+L` | Analyze selected code |
| Improve Code | `Ctrl+Shift+I` | Get improvement suggestions |
| Explain Code | - | Explain selected code |
| Settings | - | Open extension settings |

## ⚙️ Configuration

Configure in VS Code settings (`Ctrl+,`):

```json
{
  "ai-reviewer.apiUrl": "http://localhost:8000",
  "ai-reviewer.model": "gpt-4",
  "ai-reviewer.enableRAG": true,
  "ai-reviewer.enableAST": true,
  "ai-reviewer.autoAnalyze": false,
  "ai-reviewer.showSeverity": ["BLOCKER", "WARN"]
}
```

## 🔌 Backend Connection

Extension communicates with backend API:

```
POST /analyze
{
  "diffs": [...],
  "language": "python",
  "code": "..."
}
```

## 🧪 Development

### Structure
```
src/
  ├── extension.ts       # Main entry point
  ├── client.ts          # Backend API client
  ├── auth.ts            # GitHub OAuth
  ├── ui/                # UI components
  └── commands.ts        # Command handlers
```

### Testing
```bash
npm test
```

### Package Extension
```bash
npm run package
```

## 📄 License

MIT
