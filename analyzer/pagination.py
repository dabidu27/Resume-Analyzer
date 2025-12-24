from rest_framework.pagination import PageNumberPagination

#added view-specific pagination for the analysis list view. The other views have 2-page pagination, this specific view has 3-page pagination
class AnalysisListPagination(PageNumberPagination):

    page_size = 3