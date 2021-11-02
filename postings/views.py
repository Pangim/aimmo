import json
from json.decoder    import JSONDecodeError

from django.http     import JsonResponse
from django.views    import View

from postings.models import Posting, Comment
from utils           import login_decorator


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
