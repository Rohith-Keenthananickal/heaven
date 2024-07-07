from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class VideoPagination(PageNumberPagination):
    page_size = 10  # You can set the default page size here
    page_size_query_param = 'page_size'
    max_page_size = 100
