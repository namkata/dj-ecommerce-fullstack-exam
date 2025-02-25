from apps.categories.models import Category
import math


def categories_processor(request):
    categories = Category.objects.filter(is_active=True)  # Lấy danh mục đang hoạt động
    categories_parent = categories.filter(parent__isnull=True) # Lấy danh mục cha đang hoạt động
    total_categories = len(categories_parent)  # Đếm số lượng danh mục

   
    if total_categories <= 8:
        left_categories = categories[: total_categories // 2]
        right_categories = categories[total_categories // 2 :]
        categories_more_left = []
        categories_more_right = []
    else:
        left_categories = categories[:4]
        right_categories = categories[4:8]
        categories_more = categories[8:]

        # Chia Show More thành hai cột đều nhau
        mid_index = math.ceil(len(categories_more) / 2)  # Làm tròn lên để cột trái có nhiều hơn nếu số lẻ
        categories_more_left = categories_more[:mid_index]
        categories_more_right = categories_more[mid_index:]

    return {
        "categories": categories,
        "categories_parent": Category.objects.filter(
            parent__isnull=True, is_active=True
        ),
        "categories_left": left_categories,
        "categories_right": right_categories,
        "categories_more_left": categories_more_left,
        "categories_more_right": categories_more_right,
    }
