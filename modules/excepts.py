class NoFoundTrack(Exception):   
    
    def __init__(self):    
        self.err = 'Nothing was found for your query'
    
    def __str__(self):
        return self.err

class MaxTrack(Exception):   
    
    def __init__(self):    
        self.err = 'The number of tracks should not exceed 48'
    
    def __str__(self):
        return self.err


class PageError(Exception):   
    
    def __init__(self):    
        self.err = 'Only <= 11'
    
    def __str__(self):
        return self.err