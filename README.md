# npm2py-inspector

A zero-dependency **static health checker** for NPM, React, and TypeScript projects—written entirely in Python!

It reads your `package.json`, `.tsx` files, and `tsconfig.json` to flag common problems, such as missing lockfiles, usage of the `any` type in TypeScript, massive React components, and unpinned dependencies. **It never imports or executes your JavaScript/TypeScript code.**

```
$ npm2py-inspector ./my-react-app

ERROR    NPM001  package.json:1  No lockfile found. Always commit your package-lock.json or yarn.lock.
WARNING  TS001   src/App.tsx:42  Explicit 'any' type found. Use a more specific type or 'unknown'.
INFO     RCT001  src/Dashboard.tsx:1  Component file is 412 lines long. Consider breaking it into smaller sub-components.

Category scores:
  dependencies     90/100
  typescript       96/100
  react            99/100
  configuration   100/100

Overall score: 96/100  (1 error(s), 1 warning(s))
```

## Features

- **Zero runtime dependencies.** Only the Python standard library (`ast`, `re`, `json`, `pathlib`).
- **Static only.** Files are read as text. Nothing is executed using Node.js.
- **Scored.** Start at 100. Each **error** costs 10 points and each **warning** costs 4.
- **CI-friendly.** Exit code `1` on errors, and `--format json` for machine-readable output.

## Installation

Requires Python 3.9 or newer.

```bash
git clone https://github.com/mayuriphad/npm2py-inspector.git
cd npm2py-inspector
pip install .
```

## Usage

```bash
npm2py-inspector [PATH]                    # scan a directory (default: .)
npm2py-inspector PATH --format json        # JSON output for tooling
npm2py-inspector PATH --fail-under 80      # CI gate on the overall score
npm2py-inspector --list-rules
```

## License

MIT License
Copyright (c) 2026 Mayuri
