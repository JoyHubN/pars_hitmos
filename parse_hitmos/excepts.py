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
    


class MusicName(Exception):   
    
    def __init__(self):    
        self.err = 'The name of the music should only be str'
    
    def __str__(self):
        return self.err
    
class AmountErr(Exception):   
    
    def __init__(self):    
        self.err = 'The amount should only be int'
    
    def __str__(self):
        return self.err
    
class PageCount(Exception):   
    
    def __init__(self):    
        self.err = 'Page count only int'
    
    def __str__(self):
        return self.err

    
class CountTracksErr(Exception):   
    
    def __init__(self):    
        self.err = 'The count tracks should only be int'
    
    def __str__(self):
        return self.err

class RedirectErr(Exception):   
    
    def __init__(self):    
        self.err = 'Accepts only the bool type'
    
    def __str__(self):
        return self.err
    

class MaxAttempts(Exception):
    def __init__(self, max_attempts):
        self.err = f"Failed to create session after {max_attempts} attempts"
    
    def __str__(self):
        return self.err