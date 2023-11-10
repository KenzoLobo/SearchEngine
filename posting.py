class Posting:
    def __init__(self, url, id, tfidf):
        self.url = url
        self.id = id
        self.tfidf = tfidf

    def get_url(self):
        return self.url

    def get_id(self):
        return self.id

    def get_tfidf(self):
        return self.tfidf
    
    def set_tfid(self, new_tfidf ):
        self.tfid= new_tfidf
