from django.shortcuts import redirect, render, get_object_or_404
from article.models import Article, PostComment
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from myblog.forms import CommentForm

# 文章首頁
# 建立、更新、刪除、搜尋文章

# 检查用户是否是管理员
def is_admin(user):
    return user.is_staff

def homepage(request):
    articles = Article.objects.all().values()
    if articles:
        context = {"articles":articles}
        return render(request, "home.html",context)
    return render(request,"home.html")

def article_detail(request, articleid=None):
    article = get_object_or_404(Article, article_id=articleid)
    comments = PostComment.objects.filter(article_id=article.article_id, parent_comment__isnull=True).order_by('timestamp')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            parent_comment_id = request.POST.get('parent_comment_id')
            if parent_comment_id:
                comment.parent_comment = PostComment.objects.get(id=parent_comment_id)
            comment.save()
            return redirect('Article_Detail', articleid=articleid)
    else:
        form = CommentForm()
    return render(request,"article/article_detail.html",{'article':article,'comments':comments,'form': form})

@user_passes_test(is_admin)
def create_article(request):
    if request.method=='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article(title=title, 
                          content=content)
        article.save()
        return render(request,'article/create_article.html',{"message":"文章建立成功"})
        
    return render(request,'article/create_article.html')

@user_passes_test(is_admin)
def delete_article(request, articleid):
    if request.method=='POST':
        article = get_object_or_404(Article, article_id=articleid)
        article.delete()
        return redirect('Home')
    return render(request, "home.html")
        


