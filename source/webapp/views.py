from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import ArticleForm, CommentForm
from webapp.models import Article, Comment
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=pk)
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                category=form.cleaned_data['category']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'create.html', context={'form': form})


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        form = ArticleForm(data={
            'title': article.title,
            'author': article.author,
            'text': article.text,
            'category': article.category_id
        })
        return render(request, 'update.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.author = form.cleaned_data['author']
            article.text = form.cleaned_data['text']
            article.category = form.cleaned_data['category']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'update.html', context={'form': form, 'article': article})


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        return render(request, 'delete.html', context={'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        article.delete()
        return redirect('index')


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comment/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=form.cleaned_data['article'])

            return redirect('comment_view', pk=comment.pk)
        else:
            return render(request, 'comment/create.html', context={'form': form})


class CommentView(TemplateView):
    template_name = 'comment/comment.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['comments'] = get_object_or_404(Comment, pk=pk)
        return context


class CommentUpdateView(TemplateView):

    def get(self, request, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        form = CommentForm(data={'author': comment.author,
                                 'text': comment.text,
                                 'article': comment.article})
        return render(request, 'comment/update.html', context={'form': form, 'comment': comment})

    def post(self, request, **kwargs):
        comments = get_object_or_404(Comment, pk=kwargs['pk'])
        form = CommentForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            comments.author = data['author']
            comments.text = data['text']
            comments.article = data['article']
            comments.save()
            return redirect('comment_view',  pk=comments.pk)
        else:
            return render(request, 'comment/update.html', context={'form': form})


class CommentDeleteView(TemplateView):
    def get(self, request, *args, **kwargs):
        comments = get_object_or_404(Comment, pk=kwargs['pk'])
        return render(request, 'comment/delete.html', context={'comment': comments})

    def post(self, request, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        try:
            comment.delete()
            return redirect('comment_view')
        except Exception:
            return redirect('comment_view')
