from elasticsearch import Elasticsearch 
from elasticsearch_dsl import Search, Q 

def esearch(firstname="", gender=""):  

    # creating a connection to the Elasticsearch server and assign it to the client variable    
    client = Elasticsearch()      
    q = Q("bool", should=[Q("match", firstname=firstname),       
    Q("match", gender=gender)], minimum_should_match=1)  
    s = Search(using=client, index="bank").query(q)[0:20] 
    response = s.execute()
    print('Total hits found.', response.hits.total)     
    search = get_results(response)    
    return search  

def getArticals():
    client = Elasticsearch()  
   
    res = Search(using=client, index="blog").query()[0:50]
    response = res.execute()
    print('Total hits found.', response.hits.total)     
    results = [] 
    i=0
    for hit in response: 
        i=+1
        print('hit', i, hit)
        result_tuple = ( hit.title, hit.body, hit.tags)    
        results.append(result_tuple)  

    print(results)
    return results  

def getSearchData(title="", body=""):
    client = Elasticsearch()      
    q = Q("bool", should=[Q("match", title=title),       
    Q("match", body=body)], minimum_should_match=1)  
    s = Search(using=client, index="blog").query(q)[0:20] 
    
    response = s.execute()
    print("*****************", q, s)
    print('Total hits found.', response.hits.total, response)    
    results = [] 
   
    for hit in response: 
       
        result_tuple = ( hit.title, hit.body, hit.tags)   
        print(result_tuple) 
        results.append(result_tuple) 
    return results  

def get_results(response): 

    results = []  
    for hit in response: 
        result_tuple = (hit.firstname + ' ' + hit.lastname,
        hit.email, hit.gender, hit.address)    
        results.append(result_tuple)  
    return results

if __name__ == '__main__':  
    print("Opal guy details:\n", esearch(firstname = "opal"))
    print("the first 20 f gender details:\n", esearch(gender = "f"))