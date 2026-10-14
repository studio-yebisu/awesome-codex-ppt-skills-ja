from .agentic import DeckPlan, DesignProfile, RequestEnvelope, SlidePlan, verify_assets
from .api import DeckSummary, Presentation, SlideRef
from .errors import SlidesError
from .model import OperationBatch, OperationReport
from .validator import ValidationReport

CONTRACT_VERSION = "2026.03-alpha"

__all__ = [
    "Presentation",
    "SlidesError",
    "CONTRACT_VERSION",
    "DeckPlan",
    "DeckSummary",
    "DesignProfile",
    "OperationBatch",
    "OperationReport",
    "RequestEnvelope",
    "SlidePlan",
    "SlideRef",
    "ValidationReport",
    "verify_assets",
]
