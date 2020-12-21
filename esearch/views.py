from django.http import HttpResponse 
from django.shortcuts import render
from .es_call import esearch, getArticals, getSearchData
# Create your views here.

def Blog(request):
   
    # print("------------------------",  Article().is_published())
    if (request.method == 'POST'):
        print('post**********************', request.POST.get('title'))
        title = request.POST.get('title')
        body = request.POST.get('body')
        tags = request.POST.get('tags')
        lines = request.POST.get('lines')
        id = request.POST.get('id')

        article = Article(meta={'id': id}, title=title, tags=tags, body=body, lines=lines)
        article.published_from = datetime.now()
        article.save()
        print("***********ARTICLE************", article)
    
    results = getArticals()
    print(results)
    context = {'results': results, 'count': len(results)}

    return render(request,  'esearch/create_user.html', context)

def search_blog(request):
    results = []
    title = ""
    body = ""

    if request.GET.get('print_btn'):
        print("**********DELETE***********", request, request.GET.get('mytuple'))


    if request.GET.get('title') and request.GET.get('body'):
        title = request.GET['title']
        body = request.GET['body']
    elif request.GET.get('title'):
        title = request.GET['title']
    elif request.GET.get('body'):
        body = request.GET['body']

    search_term = title or body
    results = getSearchData(title=title, body=body)
    print(results)
    context = {'results': results, 'count': len(results), 'search_term':  search_term}
    return render(request,  'esearch/index.html',  context)


def search_index(request):
    results = []
    name_term = ""
    gender_term = ""

    if request.GET.get('name') and request.GET.get('gender'):
        name_term = request.GET['name']
        gender_term = request.GET['gender']
    elif request.GET.get('name'):
        name_term = request.GET['name']
    elif request.GET.get('gender'):
        gender_term = request.GET['gender']

    search_term = name_term or gender_term
    results = esearch(firstname = name_term, gender=gender_term)
    print(results)
    context = {'results': results, 'count': len(results), 'search_term':  search_term}
    return render(request,  'esearch/index.html',  context)


from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Article(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Index:
        name = 'blog'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from
Article.init()

# create and save and article
# article = Article(meta={'id': 42}, title='Hello world!', tags=['test'])
# article.body = ''' looong text '''
# article.published_from = datetime.now()
# article.save()

# article = Article.get(id=42)
# print(article.is_published())


# Display cluster health
# print(connections.get_connection().cluster.health())