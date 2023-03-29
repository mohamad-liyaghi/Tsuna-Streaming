from django.db import models
from django.core.cache import cache


class VoteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def upvotes(self):
        return self.get_queryset().filter(choice="u").count()
    
    def downvotes(self):
        return self.get_queryset().filter(choice="d").count()
    
    def get_from_cache(self, object, user):
        '''
            Check cache and db to find a vote
        '''
        key = f'vote:{object.token}:{user.token}'

        # get vote from cache
        cached_vote = cache.get(key=key)

        # if vote exists in cache
        if cached_vote:
            # Votes with status deleted means that they exist in db and we expect them to be deleted with celery
            if cached_vote.get('deleted'):
                return None
            
            return cached_vote

        # check if vote exists in db    
        # if exists, add to cache
        elif (vote:=object.votes.filter(user=user).first()):
    
            cache.set(
                key=key,
                value={
                    'source' : 'database',
                    'choice' : vote.choice,
                    'deleted' : False
                },
                timeout= 60 * 60 * 60 * 24 # 24 hours
            )
            return cache.get(key)

        return None
    
    def create_in_cache(self, object, user, choice:str):
        '''Create a vote in cache, then celery will insert it into db'''

        key = f'vote:{object.token}:{user.token}'
        # get vote from cache or db
        cached_vote = self.get_from_cache(object, user)
        
        # if user has already voted
        if cached_vote:

            # delete the vote if cache is getting saved twice (eg: user likes a video twice)
            if cached_vote.get('choice') == choice:
                # set a cache for deleting object from cache with celery
                if cached_vote.get('source') == 'database':
                    cache.set(
                        key=key,
                        value={
                            'source' : 'cache',
                            'choice' : choice,
                            'deleted' : True
                        },
                        timeout= 60 * 60 * 60 * 24 
                    ) 

                return None
            
            # Update a vote if user voted with different val
            elif cached_vote.get('choice') != choice:
                # update the vote
                cache.set(
                    key=key,
                    value={
                        'source' : 'cache',
                        'choice' : choice,
                        'deleted' : False
                    },
                    timeout= 60 * 60 * 60 * 24 
                ) 
                  
        # if cache does not exist create a vote cache
        else:    
            cache.set(
                key=key,
                value={
                    'source' : 'cache',
                    'choice' : choice,
                    'deleted' : False
                },
                timeout= 60 * 60 * 60 * 24 
            ) 