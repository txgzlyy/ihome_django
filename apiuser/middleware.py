# coding=utf-8
# from django.http import HttpResponseRedirect
#
#
# class ihome_middleware(object):
#     def process_view(self,request, view_func, *args, **kwargs):
#         path = request.get_full_path()
#         paths = [
#             '/',
#             '/v1.0/users/',
#             '/v1.0/imagecode',
#             '/v1.0/smscode/',
#             '/v1.0/sessions/',
#             '/v1.0/session/',
#         ]
#         if path not in(paths):
#             return HttpResponseRedirect('/v1.0/sessions/')