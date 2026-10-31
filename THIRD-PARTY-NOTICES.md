# Third-party notices

The game source is distributed under the repository LICENSE. The classic browser bundle contains project-owned application code and no separately fetched runtime library.

Build tooling includes TypeScript (Apache-2.0), Vite (MIT), Rollup (MIT) and esbuild (MIT). Tooling remains a developer dependency and is not copied as node_modules into browser releases. Exact versions and transitive dependencies are recorded in package-lock.json; their license texts remain available in the corresponding installed package directories. Python pytest, Playwright and JSON Schema packages are verification dependencies, not browser runtime assets.
