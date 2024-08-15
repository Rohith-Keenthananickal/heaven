from rest_framework import serializers
from .models import Video
# from rest_framework.pagination import PaginationSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class PaginatedVideoSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = VideoSerializer(many=True)


class CustomPagination(PageNumberPagination):
    page_size = 5  # Default page size if not provided in the request
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        # Get the page number from the request body instead of query params
        self.page = int(request.data.get('page', 1))  # Default to page 1 if not provided
        self.page_size = int(request.data.get('number_of_requests', self.page_size))  # Get page size from the body
        self.request = request

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page.paginator.per_page,
            'results': data
        })