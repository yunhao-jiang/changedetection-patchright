# changedetection-patchright

A Docker wrapper for [changedetection.io](https://github.com/dgtlmoon/changedetection.io) that replaces Playwright with [patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) as the browser automation backend.

> ⚠️ Warning:
> This project is a personal project and has no official support from changedetection.io. Please use at your own risks.

## What This Is

[changedetection.io](https://github.com/dgtlmoon/changedetection.io) is a self-hosted web change detection and monitoring application. This project produces a drop-in Docker image that swaps out Playwright for patchright — a patched Playwright fork designed to avoid bot detection — without requiring any changes to changedetection.io itself.

The swap is achieved by:
1. Installing `patchright` and uninstalling `playwright` in the Docker image.
2. Injecting a [`sitecustomize.py`](sitecustomize.py) module that aliases the `playwright` namespace to `patchright` at import time, so changedetection.io continues to work unchanged.

## Usage

### Pull the pre-built image

```bash
docker pull ghcr.io/yunhao-jiang/changedetection-patchright:latest
```

### Run

```bash
docker run -d \
  -p 5000:5000 \
  -v changedetection-data:/datastore \
  ghcr.io/yunhao-jiang/changedetection-patchright:latest
```

For configurations, usage, enviornment variable, etc., please visit the [official repo](github.com/dgtlmoon/changedetection.io).

### Build locally

```bash
docker build -t changedetection-patchright .
```

## Image Tags

Images are published to the [GitHub Container Registry](https://ghcr.io/yunhao-jiang/changedetection-patchright) with the following tags:

| Tag | Description |
|-----|-------------|
| `latest` | Latest build tracking the upstream `latest` image |
| `<version>` | Pinned to a specific changedetection.io release (e.g. `0.54.5`) |
| `sha-<short>` | Pinned to a specific upstream image digest (e.g. `sha-7ce66cb803e0`) |

## Automatic Updates

A [GitHub Actions workflow](.github/workflows/build.yml) polls Docker Hub hourly for a new upstream `dgtlmoon/changedetection.io:latest` digest. When a change is detected the image is automatically rebuilt and pushed to GHCR, keeping this image in sync with upstream releases.

## How It Works

### `sitecustomize.py`

Python automatically executes `sitecustomize.py` on interpreter startup. This file aliases the `playwright` module to `patchright`:

```python
import sys
import patchright
import patchright.async_api
import patchright._impl._errors

sys.modules["playwright"] = patchright
sys.modules["playwright.async_api"] = patchright.async_api
sys.modules["playwright._impl._errors"] = patchright._impl._errors
```

Any code that does `import playwright` therefore transparently receives `patchright` instead, with no source-code changes required in changedetection.io.


## Credits

- [changedetection.io](https://github.com/dgtlmoon/changedetection.io) by [@dgtlmoon](https://github.com/dgtlmoon) — the underlying web change detection application.
- [patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) — the patched Playwright fork used as the browser automation backend.

## License

This project contains only Docker and Python glue code. Please refer to the upstream projects for their respective licenses.
