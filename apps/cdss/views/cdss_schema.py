from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cdss.engines.clinical_schema import (
    MEDICAL_HISTORY_CHOICES,
    COMPLAINT_REGISTRY,
    EXAM_SCHEMA,
)


class CdssSchemaAPIView(APIView):
    """
    GET /api/v1/cdss/schema/

    Returns all structured choices for the 3 wizard sections:
      - section1: medical history chip options (systemic_conditions, habits, allergies, etc.)
      - section2: per-department complaint codes and labels
      - section3: per-department adaptive examination fields with allowed values

    The frontend should call this once on app load and cache the result.
    """

    def get(self, request, *args, **kwargs):
        return Response({
            "section1_medical_history": MEDICAL_HISTORY_CHOICES,
            "section2_complaints": COMPLAINT_REGISTRY,
            "section3_examination": EXAM_SCHEMA,
        })
