import requests as req
from decouple import config

class TMDB:
    def __init__(self):
        self.URL = config('TMDB_URL')
        self.KEY = config('TMDB_API_KEY')
        # self.res = {"status":200,"data":{},"message":""}
        
    def fetch_popular_movies(self,page=1):
        url = self.URL+"movie/popular?api_key="+self.KEY+"&language=en-US&page="+str(page)
        try:
            print("FETCHING POPULAR MOVIES: ",url)
            res = req.get(url)
            # print(res.json())
            return {"status":200,"data":res.json(),"message":"Success"}
        except Exception as ex:
            print("Failed to fetch Popular Movies!",ex)
            return {"status":400,"data":{},"message":"Failed to fetch Popular Movies"}
        
    def search_movies(self,keyword,page=1):
        url = self.URL+f"search/movie?api_key={self.KEY}&language=en-US&language=en-US&query={keyword}&page={page}"
        try:
            # print("Searching:",url)
            res = req.get(url)
            # print("RES:",res.json())
            return {"status":200,"data":res.json(),"message":"Success"}
        except Exception as ex:
            print("Failed to search movies!",ex)
            return {"status":400,"data":{},"message":f"Failed to search movies for {keyword}!"}
        

        
    def get_stream_url(self,movieId):
        # return 'https://www.youtube.com/watch?v=JPZxMhZ4KDw&list=RD6QoBpFUX6CE&index=11'
        return f"https://www.2embed.ru/embed/tmdb/movie?id={movieId}"
    
    def get_backdrop_path_url(self,backdropPath):
        return f"https://image.tmdb.org/t/p/w300{backdropPath}"