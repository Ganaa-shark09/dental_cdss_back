from django.urls import path
from apps.treatment_plans.views.treatment_plan import (
    TreatmentPlanListCreateAPIView,
    TreatmentPlanDetailAPIView,
)

urlpatterns = [
    path(
        "", TreatmentPlanListCreateAPIView.as_view(), name="treatment-plan-list-create"
    ),
    path(
        "<uuid:treatment_plan_id>/",
        TreatmentPlanDetailAPIView.as_view(),
        name="treatment-plan-detail",
    ),
]
