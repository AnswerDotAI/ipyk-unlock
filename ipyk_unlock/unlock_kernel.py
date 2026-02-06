from ipykernel.ipkernel import IPythonKernel

class UnlockKernel(IPythonKernel):
    implementation = "unlock-kernel"
    implementation_version = "0.1.0"
    language = "python"
    language_version = "3.x"
    language_info = dict(name="python", mimetype="text/x-python",
                         file_extension=".py", nbconvert_exporter="python")
    banner = "Unlock kernel"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import contextlib
        self._main_asyncio_lock = contextlib.nullcontext()
