from django.db import models


class VoteQueryset(models.QuerySet):
    
    def upvotes(self):
        return self.filter(choice="u").count()
    
    def downvotes(self):
        return self.filter(choice="d").count()