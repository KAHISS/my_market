import math
from django.core.paginator import Paginator


def make_pagination_range(page_range, qty_pages, current_page):
    total_pages = len(page_range)
    middle = math.ceil(qty_pages / 2)

    # Calcula início e fim do range
    start = current_page - middle
    end = current_page + middle - 1

    # Garante que não passamos dos limites
    if start < 1:
        start = 1
        end = qty_pages
    if end > total_pages:
        end = total_pages
        start = max(total_pages - qty_pages + 1, 1)

    pagination = page_range[start - 1:end]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'total_pages': total_pages,
        'current_page': current_page,
        'qty_pages': qty_pages,
        'first_page_out_of_range': start > 1,
        'last_page_out_of_range': end < total_pages,
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
