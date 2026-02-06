from ipykernel.kernelapp import IPKernelApp
from traitlets import Type


class UnlockKernelApp(IPKernelApp):
    kernel_class = Type("ipyk_unlock.unlock_kernel.UnlockKernel", klass="ipykernel.kernelbase.Kernel",
                        help="Kernel subclass used by this launcher.").tag(config=True)
    subcommands = {"install": ("ipyk_unlock.kernelspec.InstallUnlockKernelSpecApp", "Install the Unlock kernel")}


launch_new_instance = UnlockKernelApp.launch_instance
