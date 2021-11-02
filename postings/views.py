import json
from json.decoder import JSONDecodeError

from django.db.models.query_utils import Q
from django.http                  import JsonResponse
from django.views                 import View
from django.core.paginator        import Paginator 

from users.models                 import User 
from postings.models              import Category, Posting, Comment
from utils                        import login_decorator

class CommentView(View):
    @login_decorator
    def post(self, request, posting_id):
        try:
            data              = json.loads(request.body)
            user_id           = request.user.id
            posting_id        = posting_id
            parent_comment_id = data.get('parent_comment_id')
            content           = data['content']

            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message': 'POSTING_DOES_NOT_EXIST'}, status=404)

            Comment.objects.create(
                user_id           = user_id,
                posting_id        = posting_id,
                parent_comment_id = parent_comment_id,
                content           = content
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get(self, request, posting_id):
        comments = Comment.objects.filter(posting_id=posting_id, parent_comment= None)
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 100))

        if not Posting.objects.filter(id=posting_id).exists():
            return JsonResponse({'message': 'POSTING_DOES_NOT_EXIST'}, status=404)
       
        comment_list = [{
            'comment_id'          : comment.id,  
            'user_name'           : comment.user.name,
            'content'             : comment.content,
            'created_at'          : comment.created_at,
            'nested_comment_list' : [{
                'comment_id' : nested_comment.id,
                'user_name'  : nested_comment.user.name,
                'content'    : nested_comment.content,
                'created_at' : nested_comment.created_at 
            } for nested_comment in Comment.objects.filter(parent_comment=comment)][offset:offset+limit]   
        } for comment in comments][offset:offset+limit]

        return JsonResponse({'comment_list': comment_list}, status=200)

    @login_decorator
    def delete(self, request):
        try:
            user_id    = request.user.id
            comment_id = request.GET.get('id')
            comment    = Comment.objects.get(id=comment_id)
            
            if user_id != comment.user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
            comment.delete()

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except Comment.DoesNotExist:
            return JsonResponse({'message': 'COMMENT_DOES_NOT_EXIST'}, status=404)

    @login_decorator
    def patch(self, request):
        try:    
            data       = json.loads(request.body)
            user_id    = request.user.id
            comment_id = request.GET.get('id')
            comment    = Comment.objects.get(id=comment_id)
            content    = data['content']

            if user_id != comment.user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)  

            comment.content = content
            comment.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201)  
        
        except Comment.DoesNotExist:
            return JsonResponse({'message': 'COMMENT_DOES_NOT_EXIST'}, status=404)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

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
            page   = request.GET.get('page', 1)

            if search:
                q.add(Q(title__icontains = search), q.AND) 
                q.add(Q(content__icontains = search), q.OR) 
                category_id = [ category.id
                    for category in Category.objects.filter(name__icontains = search)]
                q.add(Q(category_id__in = category_id), q.OR) 

        except:
            return JsonResponse({"message" : "Error"}, status = 400)

        postings_list = Posting.objects.filter(q).select_related('user', 'category')
        paginator = Paginator(postings_list, 10)
        postings = paginator.get_page(page) 

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