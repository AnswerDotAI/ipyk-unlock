# ipyk-unlock

Minimal custom `ipykernel` launcher that swaps in `ipyk_unlock.unlock_kernel.UnlockKernel`.

## Run

```bash
python -m ipyku_launcher -f /path/to/connection.json
```

## Install kernelspec

```bash
python -m ipyku_launcher install --sys-prefix
```

Default kernelspec name is `python3-unlock` (on Python 3).

## Install (local)

```bash
pip install -e .
```

For release tooling:

```bash
pip install -e .[dev]
```

## Use in a kernelspec

Set `argv` in `kernel.json` to:

```json
["python", "-m", "ipyku_launcher", "-f", "{connection_file}"]
```

