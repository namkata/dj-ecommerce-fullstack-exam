from apps.categories.models import Category

def categories_processor(request):
    return {"categories": Category.objects.all()}
