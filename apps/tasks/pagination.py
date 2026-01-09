from rest_framework.pagination import CursorPagination


class TaskPagination(CursorPagination):
    page_size = 20
    ordering = "-priority", "-created_at"
