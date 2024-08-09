

from .models import Genre

def genre_processor(request):
    return {'genres': Genre.objects.all()}
