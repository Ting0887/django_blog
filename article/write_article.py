from models import Article, Comment

def populate():
    Article.objects.all().delete()
    Comment.objects.all().delete()
    titles = ['如何學習新技術?','身為工程師的工作技能','刷題技巧?']
    comments = ['推這篇','想分享','學習程式需要花時間']
    for title in titles:
        article = Article()
        article.title = title
        for j in range(20):
            article.content += title + '\n'
        article.save()
        for comment in comments:
            Comment.objects.create(article=article, content=comment)
    print('done!')

if __name__ == '__main__':
    populate()