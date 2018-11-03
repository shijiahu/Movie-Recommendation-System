
# 1. Data Processing
# data[user][movie]=rating
# key = user, value = {movie : rating} 

data ={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
     'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
     'The Night Listener': 3.0},
             
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
     'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
     'You, Me and Dupree': 3.5}, 
             
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
     'Superman Returns': 3.5, 'The Night Listener': 4.0},
             
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
     'The Night Listener': 4.5, 'Superman Returns': 4.0, 
     'You, Me and Dupree': 2.5},
             
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
     'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
     'You, Me and Dupree': 2.0},
              
    'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
     'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
             
    'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
}


# 2. filter movies

def transformdata(data):
    '''
    Similarity among movies is same as similarity among users
    Exchange user and movie
    '''   
    newdata = {}
    users ={}
    for person in data:
        for movie in data[person]:
            #Initialization
            newdata.setdefault(movie,{})
            #Exchange user and movie
            newdata[movie][person] = data [person][movie]  
    return newdata

'''
print(transformdata(data))

{'Lady in the Water': {'Lisa Rose': 2.5, 'Jack Matthews': 3.0, 'Michael Phillips': 2.5, 'Gene Seymour': 3.0, 'Mick LaSalle': 3.0}, 
'Snakes on a Plane': {'Jack Matthews': 4.0, 'Mick LaSalle': 4.0, 'Claudia Puig': 3.5, 'Lisa Rose': 3.5, 'Toby': 4.5, 'Gene Seymour': 3.5, 'Michael Phillips': 3.0},
 'Just My Luck': {'Claudia Puig': 3.0, 'Lisa Rose': 3.0, 'Gene Seymour': 1.5, 'Mick LaSalle': 2.0}, 
 'Superman Returns': {'Jack Matthews': 5.0, 'Mick LaSalle': 3.0, 'Claudia Puig': 4.0, 'Lisa Rose': 3.5, 'Toby': 4.0, 'Gene Seymour': 5.0, 'Michael Phillips': 3.5}, 
 'The Night Listener': {'Jack Matthews': 3.0, 'Mick LaSalle': 3.0, 'Claudia Puig': 4.5, 'Lisa Rose': 3.0, 'Gene Seymour': 3.0, 'Michael Phillips': 4.0}, 
'You, Me and Dupree': {'Jack Matthews': 3.5, 'Mick LaSalle': 2.0, 'Claudia Puig': 2.5, 'Lisa Rose': 2.5, 'Toby': 1.0, 'Gene Seymour': 3.5}}
'''


from math import sqrt
def sim_distance(data,person1,person2):
    '''
    Euclidean Distance Similarity
    '''
    # Common movies with person1 and person2
    commonmovies = [ movie for movie in data[person1] if movie in data[person2]] 
    if len(commonmovies)== 0: return 0 
    #Sum of squares
    sumSq =sum([pow(data[person1][movie] -data[person2][movie],2) for movie in commonmovies ] )
    #？？？？？？？
    sim = 1/(1+ sqrt(sumSq))
    return sim 

def sim_pearson(data,person1,person2):
    '''
    计算上面格式的数据里的两个用户相似度.
    基于用户过滤思路：找出两个用户看过的相同电影的评分，从而进行按pearson公式求值。那些非公共电影不列入求相似度值范围。
    基于电影过滤思路：找过两部电影相同的观影人给出的评分，从而按pearson公式求值
    返回：评分的相似度，[-1,1]范围，0最不相关，1，-1为正负相关，
    等于1时，表示两个用户完全一致评分
    这里的data格式很重要，这里计算相似度是严格按照上面data格式所算。
    此字典套字典格式，跟博客计算单词个数 存储格式一样 
    '''

    # Common movies with person1 and person2
    commonmovies = [ movie for movie in data[person1] if movie in data[person2]] 
    
    # Number of movie seen by both person1 and person2
    n = float(len(commonmovies))
    if n==0: 
        return 0
    
    '''
    Pearson Correlation Coefficient
    '''
    # 分布对两个用户的公共电影movie分数总和
    sum1 = sum([data[person1][movie]for movie in commonmovies])  
    sum2 = sum([data[person2][movie]for movie in commonmovies])
    
    # 计算乘积之和
    sum12 = sum([data[person1][movie]*data[person2][movie] for movie in commonmovies])
    
    #计算平方和
    sum1Sq = sum([ pow(data[person1][movie],2 ) for movie in commonmovies ])        
    sum2Sq = sum([ pow(data[person2][movie],2 ) for movie in commonmovies ]) 
    
    #计算分子        
    num = sum12 - sum1*sum2/n
    #分母
    den = sqrt((sum1Sq - pow(sum1,2)/n)*(sum2Sq - pow(sum2,2)/n))
    if den==0:  return 0                
    
    return num/den


# Return top matched for a movie
# default return 5 movie and using pearson similarity 
def topmatches(data, givenperson, returnernum = 5, simscore = sim_pearson):
    '''
    input: (based on user filter) recommend 5 users
            ------given a person, return people with the same interests
            OR  
            (based on movie filter) recommend 5 movies
            ------given a movie, return movie with similar movies
    '''

    # Result list
    usersscores =[(simscore(data,givenperson,other),other) for other in data if other != givenperson ]

    # sort the list in the descending order
    usersscores.sort(reverse=True)
    
    # default return top 5
    return usersscores[0:returnernum]



'''
moviedata = transformdata(data)

# find the similar movie with 'Superman Returns'
print(topmatches(moviedata, 'Superman Returns'))

Result:
[(0.6579516949597695, 'You, Me and Dupree'), (0.4879500364742689, 'Lady in the Water'), 
(0.11180339887498941, 'Snakes on a Plane'), (-0.1798471947990544, 'The Night Listener'), (-0.42289003161103106, 'Just My Luck')]
negative number means hate the movie...

'''


# based on "topmatches" function, return all movies matches result

def calSimilarItems(data,num=10):
    moviedata = transformdata(data)
    ItemAllMatches = {}
    for movie in moviedata:
         ItemAllMatches.setdefault(movie,[])
         # for each movie, calculate its match movie set, using Euclidean Distance Similarity or Pearson
         ItemAllMatches[movie] = topmatches(moviedata, movie, num,simscore = sim_pearson)
    return ItemAllMatches

print(calSimilarItems(data))
'''
# Dictionary for movies similarity： key = movie ,value = [(othermovie,simscore)]。

print(calSimilarItems(data))

{'Lady in the Water': [(0.7637626158259785, 'Snakes on a Plane'), (0.4879500364742689, 'Superman Returns'), (0.3333333333333333, 'You, Me and Dupree'), (-0.6123724356957927, 'The Night Listener'), (-0.9449111825230676, 'Just My Luck')],
 'Snakes on a Plane': [(0.7637626158259785, 'Lady in the Water'), (0.11180339887498941, 'Superman Returns'), (-0.3333333333333333, 'Just My Luck'), (-0.5663521139548527, 'The Night Listener'), (-0.6454972243679047, 'You, Me and Dupree')], 
'Just My Luck': [(0.5555555555555556, 'The Night Listener'), (-0.3333333333333333, 'Snakes on a Plane'), (-0.42289003161103106, 'Superman Returns'), (-0.4856618642571827, 'You, Me and Dupree'), (-0.9449111825230676, 'Lady in the Water')],  .........
'''







