#  A Minimal Reproducible Example for uv Issue 14883

Issue: https://github.com/astral-sh/uv/issues/14883

Reproduce:

```bash
make foo-publish
make bar-sync
```

Error:

```bash
× Failed to download `foo==0.1.0`
╰─▶ Hash mismatch for `foo==0.1.0`

    Expected:
      sha256:e6a87f2bc51bda97f0fd26303adb3053b114daa92620d924263f08c3587eb005

    Computed:
      sha256:b2a09ff57ec883aaffd9a9ec985648724b52fef68d995cdc0e96dbedfa426d1b
help: `foo` (v0.1.0) was included because `bar` (v0.1.0) depends on `foo`
```
