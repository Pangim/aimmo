from django.db    import models

from core.models  import TimeStampModel
from users.models import User

class Category(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'
    
    def __str__(self):
        return self.name

class Posting(TimeStampModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    views    = models.IntegerField(default=0)
    content  = models.TextField()

    class Meta:
        db_table = 'postings'
    
    def __str__(self):
        return self.title

class Comment(TimeStampModel):
    posting        = models.ForeignKey(Posting, on_delete=models.CASCADE)
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    content        = models.CharField(max_length=500)
    
    class Meta:
        db_table = 'commnets'