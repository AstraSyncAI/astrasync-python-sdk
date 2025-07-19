"""
AstraSync SDK - AI Agent Registration on Blockchain
"""
from astrasync.core import AstraSync
from astrasync.utils.detector import detect_agent_type, normalize_agent_data

__version__ = "0.2.1"
__all__ = ["AstraSync", "detect_agent_type", "normalize_agent_data"]
