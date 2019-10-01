from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from webapp.models import Article
from webapp.forms import ArticleForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class View(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=context_pk)
        return context


class ArticleCreateView(View):

    def get(self, request, **kwargs):
        form = ArticleForm()
        return render(request, 'create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            issue = Article.objects.create(title=data['title'],
                                           author=data['author'],
                                           text=data['text'])
            return redirect('article_view', pk=issue.pk)
        else:
            return render(request, 'create.html', context={'form': form})


class ArticleUpdateView(TemplateView):

    def get(self, request, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        form = ArticleForm(data={'title': article.summary,
                                 'author': article.author,
                                 'text': article.text})

        return render(request, 'update.html', context={'form': form, 'issue': issue})

    def post(self, request, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            article.title = data['title']
            article.author = data['author']
            article.text = data['text']
            article.save()
            return redirect('issue_view', pk=article.pk)
        else:
            return render(request, 'update.html', context={'form': form})


class ArticleDeleteView(TemplateView):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        return render(request, 'delete.html', context={'article': article})

    def post(self, request, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])

        article.delete()
        return redirect('index')