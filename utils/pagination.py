import math
from django.core.paginator import Paginator


def make_pagination_range(page_range, qty_pages, current_page):
    middle = math.ceil(qty_pages / 2)
    start = current_page - middle
    end = current_page + middle
    total_pages = len(page_range)

    start_offset = abs(start) if start < 0 else 0

    if start < 0:
        start = 0
        end += start_offset
    if end >= total_pages:
        start = start - abs(total_pages - end)

    pagination = page_range[start:end]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'start': start,
        'end': end,
        'total_pages': total_pages,
        'current_page': current_page,
        'qty_pages': qty_pages,
        'middle': middle,
        'start_offset': start_offset,
        'first_page_out_of_range': current_page > middle,
        'last_page_out_of_range': end < total_pages
    }


def make_pagination(request, queryset, per_page, qty_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page
    )
    return page_obj, pagination_range
