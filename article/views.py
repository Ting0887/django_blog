from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from zmq import Message
from article.models import Article, ArticleForm, Comment
from account.views import admin_required
from django.contrib import messages
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'about.html')

def article(request):
    articles = {article:Comment.objects.filter(article=article) for article in Article.objects.all()}
    context = {'articles':articles}
    print(context)
    return render(request, 'article.html', context)

@admin_required
def articleCreate(request):
    if request.method == 'GET':
        return render(request, 'articleCreate.html', {'articleForm':ArticleForm()})
    
    articleForm = ArticleForm(request.POST)
    if not articleForm.is_valid():
        return render(request, 'articleCreate.html', {'articleForm':articleForm})
    articleForm.save()
    messages.success(request, '已新增文章')
    return redirect('/article/')

def articleRead(request, articleId):
    article = get_object_or_404(Article, id=articleId)
    context = {'article':article,
                'comments':Comment.objects.filter(article=article)}
    
    return render(request, 'articleRead.html', context)

@admin_required
def articleUpdate(request, articleId):
    article = get_object_or_404(Article, id=articleId)
    if request.method == 'GET':
        articleForm = ArticleForm(instance=article)
        return render(request, 'articleUpdate.html', {'articleForm':articleForm})
    articleForm = ArticleForm(request.POST, instance=article)
    if not articleForm.is_valid():
        return render(request, 'articleUpdate.html', {'articleForm':articleForm})
    
    articleForm.save()
    messages.success(request, '文章已修改')
    return redirect(f'/articleRead/{articleId}/')

@admin_required
def articleDelete(request, articleId):
    if request.method == ' GET':
        return redirect('/article/')
    article = get_object_or_404(Article, id=articleId)
    article.delete()
    messages.success(request, '文章已刪除')
    return redirect('/article/')

def articleSearch(request):
    searchTerm = request.GET.get('searchTerm')
    articles = Article.objects.filter(Q(title__icontains=searchTerm) | Q(content__icontains=searchTerm))
    context = {'articles':articles}
    return render(request, 'ArticleSearch.html', context)    

@login_required
def articleLike(request, articleId):
    article = get_object_or_404(Article, id=articleId)
    #確認使用者是否有對這篇文章按讚
    if request.user not in article.likes.all():
        article.likes.add(request.user)
    elif request.user in article.likes.all():
        article.likes.remove(request.user)
    return articleRead(request, articleId)

@login_required
def commentCreate(request, articleId):
    if request.method == 'GET':
        return articleRead(request, articleId)
    comment = request.POST.get('comment')
    print(comment)
    if comment:
        comment = comment.strip()
    if not comment:
        return redirect('article:articleRead', articleId=articleId)
    article = get_object_or_404(Article, id=articleId)
    Comment.objects.create(article=article, user=request.user, content=comment)
    return redirect('articleRead', articleId=articleId)

@login_required
def commentUpdate(request, commentId):
    commentToUpdate = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=commentToUpdate.article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)
    
    if commentToUpdate.user != request.user:
        messages.error(request, '無修改權限')
        return redirect('article:articleRead', articleId = article.id)
    
    comment = request.POST.get('comment','').strip()
    if not comment:
        commentToUpdate.delete()
    else:
        commentToUpdate.content = comment
        commentToUpdate.save()
    return redirect('articleRead', articleId = article.id)

@login_required
def commentDelete(request, commentId):
    comment = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=comment.article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)
    
    if comment.user != request.user:
        messages.error(request, '無權限刪除')
        return redirect('articleRead', articleId = article.id)
    comment.delete()
    return redirect('articleRead', articleId = article.id)