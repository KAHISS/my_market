from unittest import TestCase
from pagination import make_pagination_range


class TestPagination(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_page_range_is_static_if_current_page_is_less_than_middle_page(self):
        # current_page = 3 - qty_pages = 2 - middle_page = 2
        # here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

    def test_middle_range_is_correct(self):
        # current_page = 10 - qty_pages = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # current_page = 12 - qty_pages = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_last_page_range_is_static_if_current_page_is_greater_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
