from .consultation import ConsultationListCreateAPIView, ConsultationDetailAPIView
from .tooth_complaint import (
    ToothComplaintListCreateAPIView,
    ToothComplaintBulkAPIView,
    ToothComplaintDetailAPIView,
)

__all__ = [
    "ConsultationListCreateAPIView",
    "ConsultationDetailAPIView",
    "ToothComplaintListCreateAPIView",
    "ToothComplaintBulkAPIView",
    "ToothComplaintDetailAPIView",
]
