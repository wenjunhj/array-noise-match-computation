"""Array noise matching and preamplifier decoupling SNR computation for MRI receive arrays."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("rx-array-snr-evaluation")
except PackageNotFoundError:  # running from a source tree that has not been installed
    __version__ = "0+unknown"
