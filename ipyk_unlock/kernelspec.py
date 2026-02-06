import errno
import platform
import shutil
import sys

from ipykernel import kernelspec as ipks
from jupyter_client.kernelspec import KernelSpecManager
from traitlets import Unicode

KERNEL_NAME = f"{ipks.KERNEL_NAME}-unlock"
DISPLAY_NAME = f"Python {sys.version_info[0]} (unlock)"

def install(kernel_spec_manager: KernelSpecManager | None = None, user: bool = False, kernel_name: str = KERNEL_NAME,
            display_name: str | None = None, prefix: str | None = None, profile: str | None = None,
            env: dict[str, str] | None = None, frozen_modules: bool = False) -> str:
    if kernel_spec_manager is None: kernel_spec_manager = KernelSpecManager()
    if env is None: env = {}
    if kernel_name != KERNEL_NAME and display_name is None: display_name = kernel_name

    overrides = dict(display_name=display_name or DISPLAY_NAME, argv=ipks.make_ipkernel_cmd(mod="ipyku_launcher"))
    extra_arguments = ["--profile", profile] if profile else None

    if extra_arguments:
        overrides["argv"] = ipks.make_ipkernel_cmd(mod="ipyku_launcher", extra_arguments=extra_arguments)
        if display_name is None: overrides["display_name"] = "Python %i [profile=%s] (unlock)" % (sys.version_info[0], profile)

    if sys.version_info >= (3, 11) and platform.python_implementation() == "CPython":
        if not frozen_modules:
            overrides["argv"] = ipks.make_ipkernel_cmd(mod="ipyku_launcher", extra_arguments=extra_arguments,
                                                       python_arguments=["-Xfrozen_modules=off"])
        elif "PYDEVD_DISABLE_FILE_VALIDATION" not in env: env["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

    if env: overrides["env"] = env
    path = ipks.write_kernel_spec(overrides=overrides)
    dest = kernel_spec_manager.install_kernel_spec(path, kernel_name=kernel_name, user=user, prefix=prefix)
    shutil.rmtree(path)
    return dest


class InstallUnlockKernelSpecApp(ipks.InstallIPythonKernelSpecApp):
    name = Unicode("ipyku-kernel-install")

    def start(self) -> None:
        import argparse

        parser = argparse.ArgumentParser(prog=self.name, description="Install the Unlock kernel spec.")
        parser.add_argument("--user", action="store_true", help="Install for the current user instead of system-wide")
        parser.add_argument("--name", type=str, default=KERNEL_NAME,
                            help="Specify a name for the kernelspec. This is needed to have multiple kernels.")
        parser.add_argument("--display-name", type=str, help="Specify the display name for the kernelspec.")
        parser.add_argument("--profile", type=str, help="Specify an IPython profile to load.")
        parser.add_argument("--prefix", type=str, help="Specify an install prefix for the kernelspec.")
        parser.add_argument("--sys-prefix", action="store_const", const=sys.prefix, dest="prefix",
                            help="Install to Python's sys.prefix.")
        parser.add_argument("--env", action="append", nargs=2, metavar=("ENV", "VALUE"),
                            help="Set environment variables for the kernel.")
        parser.add_argument("--frozen_modules", action="store_true", help="Enable frozen modules for faster startup.")
        opts = parser.parse_args(self.argv)
        if opts.env: opts.env = dict(opts.env)
        try:
            dest = install(user=opts.user, kernel_name=opts.name, profile=opts.profile, prefix=opts.prefix,
                           display_name=opts.display_name, env=opts.env, frozen_modules=opts.frozen_modules)
        except OSError as e:
            if e.errno == errno.EACCES:
                print(e, file=sys.stderr)
                if opts.user: print("Perhaps you want `sudo` or `--user`?", file=sys.stderr)
                self.exit(1)
            raise
        print(f"Installed kernelspec {opts.name} in {dest}")
