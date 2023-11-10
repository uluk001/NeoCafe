from .models import Branch
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import BranchSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView


class BranchListView(ListAPIView):

    @swagger_auto_schema(
        operation_summary="Get branches",
        operation_description="Use this method to get all branches",
        responses={200: BranchSerializer(many=True)}
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchCreateView(CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdminUser]

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(type=openapi.TYPE_STRING, description='Path to image'),
            'schedule': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            'address': openapi.Schema(type=openapi.TYPE_STRING),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'link_to_map': openapi.Schema(type=openapi.TYPE_STRING),
            'workdays': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'workday': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'start_time': openapi.Schema(type=openapi.TYPE_STRING),
                        'end_time': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )

    @swagger_auto_schema(
        operation_summary="Create branch",
        operation_description="Use this method to create a branch",
        request_body=manual_request_schema,
        responses={200: BranchSerializer}
    )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BranchUpdateView(UpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'id'

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(type=openapi.TYPE_STRING, description='Path to image'),
            'schedule': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            'address': openapi.Schema(type=openapi.TYPE_STRING),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'link_to_map': openapi.Schema(type=openapi.TYPE_STRING),
            'workdays': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'workday': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'start_time': openapi.Schema(type=openapi.TYPE_STRING),
                        'end_time': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )

    @swagger_auto_schema(
        operation_summary="Update branch",
        operation_description="Use this method to update a branch",
        request_body=manual_request_schema,
        responses={200: BranchSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class BranchDeleteView(generics.DestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'id'

    manual_parameters = [
        openapi.Parameter(
            name='id',
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description='Branch id'
        )
    ]

    @swagger_auto_schema(
        operation_summary="Delete branch",
        operation_description="Use this method to delete a branch",
        manual_parameters=manual_parameters,
        responses={200: BranchSerializer}
    )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BranchDetailView(generics.RetrieveAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'id'

    manual_parameters = [
        openapi.Parameter(
            name='id',
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description='Branch id'
        )
    ]

    @swagger_auto_schema(
        operation_summary="Get branch",
        operation_description="Use this method to get a branch",
        manual_parameters=manual_parameters,
        responses={200: BranchSerializer}
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
