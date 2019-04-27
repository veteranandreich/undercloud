from rest_framework.pagination import LimitOffsetPagination


class FeedLimitPagination(LimitOffsetPagination):
    max_limit = 100
    default_limit = 20
