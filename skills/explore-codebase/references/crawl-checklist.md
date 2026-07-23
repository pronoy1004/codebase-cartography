# Crawl checklist: where to look per ecosystem

Read the manifest first, then the entry points. This table tells you which files name the dependencies, scripts, and start points for each stack. Detect the stack by the manifest file present at the repo root, then follow the matching row.

## Manifests and entry points by language

| Ecosystem | Manifest / build files | Common entry points |
|-----------|------------------------|---------------------|
| JavaScript / TypeScript | `package.json` (see `scripts`, `dependencies`, `main`, `bin`), `tsconfig.json`, lockfile | `src/index`, `src/main`, `server.js`, framework bootstrap (Next `app/` or `pages/`, Nest `main.ts`), `bin/` for CLIs |
| Python | `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`, `Pipfile` | `main.py`, `app.py`, `manage.py` (Django), `wsgi.py`/`asgi.py`, `__main__.py`, `[project.scripts]` console entry points |
| Go | `go.mod`, `go.sum` | `func main()` in `main.go` or `cmd/*/main.go` |
| Java / Kotlin | `pom.xml` (Maven), `build.gradle` / `build.gradle.kts` (Gradle) | class with `public static void main`, Spring `@SpringBootApplication`, servlet mappings |
| Ruby | `Gemfile`, `*.gemspec` | `config.ru`, `bin/rails`, `config/routes.rb`, `lib/*.rb` |
| Rust | `Cargo.toml`, `Cargo.lock` | `src/main.rs` (binary), `src/lib.rs` (library), `[[bin]]` targets |
| PHP | `composer.json` | `index.php`, `public/index.php`, framework front controller (Laravel `bootstrap/app.php`) |
| C# / .NET | `*.csproj`, `*.sln`, `Directory.Build.props` | `Program.cs`, `Main`, ASP.NET `Startup.cs` / minimal API in `Program.cs` |
| Elixir | `mix.exs` | `application.ex`, `lib/*/application.ex`, router modules |

## Cross-cutting files to read early

- `README.md`, `CONTRIBUTING.md`, `docs/`: the maintainers' own map. Read it, then verify it against the code, because docs drift.
- Container and orchestration: `Dockerfile`, `docker-compose.yml`, `*.k8s.yaml`, `Procfile`. These name the runtime services and the start command.
- CI config: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`. These name the real build, test, and deploy steps.
- Config: `.env.example`, `config/`, `settings.*`, `*.toml`, `*.yaml`. These name the config surface.
- Monorepo tooling: `nx.json`, `turbo.json`, `pnpm-workspace.yaml`, `lerna.json`, Gradle `settings.gradle`, Go workspace `go.work`. These name the package boundaries.

## How to find API endpoints fast

Search for the route-definition idiom of the framework:

- Express / Fastify / Koa: `app.get(`, `router.post(`, `.route(`
- Flask / FastAPI: `@app.route`, `@router.get`, `APIRouter`
- Django: `urlpatterns`, `path(`, `re_path(`
- Spring: `@GetMapping`, `@PostMapping`, `@RequestMapping`
- Rails: `config/routes.rb`
- gRPC / protobuf: `*.proto` `service` blocks
- GraphQL: `*.graphql` schema files, `type Query`, `type Mutation`, resolver maps

## How to find outbound calls fast

Search for the client idioms: `fetch(`, `axios`, `http.Client`, `requests.get`, `HttpClient`, SDK imports (`stripe`, `aws-sdk`, `@google-cloud`), and database or queue clients (`pg`, `mongoose`, `redis`, `kafka`, `sqlalchemy`, `gorm`).
