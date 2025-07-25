default: foo-publish bar-sync

foo-publish:
	@uv --project=foo build --out-dir=/tmp/pypi/foo
	@uv run pypi-index.py /tmp/pypi

bar-sync:
	@uv --project=bar sync
