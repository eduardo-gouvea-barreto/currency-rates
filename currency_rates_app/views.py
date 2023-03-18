from django.shortcuts import render


def index(request):
    context = {'categories': ['Jan', 'Fev', 'Mar'], 'values': [[1, 3, 8], [0, 11, 2], [3, 4, 5]]}
    return render(request, 'index.html', context=context)
