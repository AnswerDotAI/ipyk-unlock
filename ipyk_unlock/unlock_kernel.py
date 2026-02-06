from ipykernel.ipkernel import IPythonKernel

from . import __version__

class UnlockKernel(IPythonKernel):
    implementation = "unlock-kernel"
    implementation_version = __version__
    language = "python"
    language_version = "3.x"
    language_info = dict(name="python", mimetype="text/x-python",
                         file_extension=".py", nbconvert_exporter="python")
    banner = "Unlock kernel"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import contextlib
        self._main_asyncio_lock = contextlib.nullcontext()
