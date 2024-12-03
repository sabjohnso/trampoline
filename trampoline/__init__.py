"""
A trampoline for simulating proper tail calls in Python
"""
from .__impl import tramp, tail, pull, tail_call


__all__=["tramp", "tail", "pull", "tail_call"]
