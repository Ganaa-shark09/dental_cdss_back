from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.treatment_plans.serializers import (
    TreatmentPlanSerializer,
    TreatmentPlanCreateSerializer,
)
from apps.treatment_plans.services import TreatmentPlanService


class TreatmentPlanListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        treatment_plans = TreatmentPlanService.list_treatment_plans()
        serializer = TreatmentPlanSerializer(treatment_plans, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TreatmentPlanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        treatment_plan = TreatmentPlanService.create_treatment_plan(
            serializer.validated_data
        )
        response_serializer = TreatmentPlanSerializer(treatment_plan)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TreatmentPlanDetailAPIView(APIView):
    def get(self, request, treatment_plan_id, *args, **kwargs):
        treatment_plan = TreatmentPlanService.get_treatment_plan_by_id(
            treatment_plan_id
        )
        serializer = TreatmentPlanSerializer(treatment_plan)
        return Response(serializer.data)
