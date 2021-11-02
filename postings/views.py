import json
from json.decoder import JSONDecodeError

from django.db.models.query_utils import Q
from django.http import JsonResponse 
from django.views import View 

from utils import login_decorator
from postings.models import Category, Posting
from users.models import User 

class PostingView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            title       = data['title']
            content     = data['content']
            category_id = Category.objects.get(id = data['category_id']).id
            category_id = data['category_id']
            user        = request.user 
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
            
        except Category.DoesNotExist:
            return JsonResponse({"message" : "CATEGORY_DOES_NOT_EXIST"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)
            
        Posting.objects.create(
            title       = title,
            content     = content,
            category_id = category_id,
            user_id     = user.id, 
        )

        return JsonResponse({"message" : "CREATED"}, status = 201)

    def get(self, request, posting_id = None):
        if posting_id == None:
            return JsonResponse({"message" : "NEED_POSTING_ID"}, status = 400)
        
        try:
            posting = Posting.objects.get(id = posting_id).select_related('')

        except Posting.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST"}, status = 400)
        
        result = {
            "id"         : posting.id,
            "title"      : posting.title,
            "content"    : posting.content,
            "category"   : posting.category.name,
            "views"      : posting.views,
            "user"       : posting.user.name,
            "views"      : posting.views,
            "created_at" : posting.created_at,
            "updated_at" : posting.updated_at
        }

        return JsonResponse({"result" : result}, status = 200)



    @login_decorator
    def patch(self, request, posting_id = None):
        if posting_id == None:
            return JsonResponse({"message" : "NEED_POSTING_ID"}, status = 400)
        
        try:
            data    = json.loads(request.body)
            user    = request.user
            posting = Posting.objects.get(id = posting_id)

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)

        except Posting.DoesNotExist:
            return JsonResponse({"message" : "POSTING_DOES_NOT_EXIST"}, status = 400)
        
        if posting.user_id != user.id:
            return JsonResponse({"message" : "FORBIDDEN"} , status = 403)
        
        posting.__dict__.update(data)
        posting.save()

        return JsonResponse({"message" : "UPDATED"}, status = 200)

    @login_decorator
    def delete(self, request, posting_id = None):
        if posting_id == None:
            return JsonResponse({"message" : "NEED_POSTING_ID"}, status = 400)

        try:
            user    = request.user
            posting = Posting.objects.get(id = posting_id)

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)

        except Posting.DoesNotExist:
            return JsonResponse({"message" : "POSTING_DOES_NOT_EXIST"}, status = 400)

        if posting.user_id != user.id:
            return JsonResponse({"message" : "FORBIDDEN"}, status = 403)

        posting.delete()

        return JsonResponse({"message" : "DELETED"}, status = 204)

class PostingListView(View):
    def get(self, request):
        q = Q()

        try:
            search = request.GET.get('search', None)
            if search:
                q.add(Q(title__icontains = search), q.AND) 
                q.add(Q(content__icontains = search), q.OR) 
                category_id = [ category.id
                    for category in Category.objects.filter(name__icontains = search)]
                q.add(Q(category_id__in = category_id), q.OR) 

        except:
            return JsonResponse({"message" : "Error"}, status = 400)

        postings = Posting.objects.filter(q).select_related('user', 'category')

        result = [{
            "id" : posting.id,
            "title" : posting.title,
            "views" : posting.views,
            "user" : posting.user.name,
            "category" : posting.category.name,
            "created_at" : posting.created_at,
            "updated_at" : posting.updated_at
        } for posting in postings]
    
        return JsonResponse({"result" : result}, status = 200)