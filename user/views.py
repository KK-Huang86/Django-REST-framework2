from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from user.serializers import UserSerializer 
from user.models import User

class UsersView(GenericAPIView):
    queryset = User.objects.all() #抓所有資料
    serializer_class = UserSerializer #叫出UserSerilalizer 做處理
    def get(self, request, *args, **krgs):
        users = self.get_queryset() # 取得所有 User 資料。
        serializer = self.serializer_class(users, many=True) # 序列化資料，`many=True` 表示有多筆資料。
        data = serializer.data # 轉成 JSON 格式。
        return JsonResponse(data, safe=False)# 回傳 JSON 格式的資料，`safe=False` 允許回傳 list。
    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)# 將資料傳入序列化器。
            serializer.is_valid(raise_exception=True)# 驗證資料有效性。
            with transaction.atomic():# 使用交易保證資料完整性。
                serializer.save()# 儲存資料到資料庫。
            data = serializer.data # 儲存後的資料。
        except Exception as e:# 例外，錯誤
            data = {'error': str(e)}
        return JsonResponse(data)
    
#FBV
# @api_view(['GET', 'POST'])
# def users_view(request):
    #if request.method == 'GET':
    #     users = User.objects.all()  # 取得所有使用者資料。
    #     serializer = UserSerializer(users, many=True)  # 序列化多筆資料。
    #     return JsonResponse(serializer.data, safe=False)  # 回傳 JSON 格式的資料。

    # elif request.method == 'POST':
    #     data = request.data  # 取得請求中的資料。
    #     try:
    #         serializer = UserSerializer(data=data)  # 將資料傳入序列化器。
    #         serializer.is_valid(raise_exception=True)  # 驗證資料有效性。
    #         with transaction.atomic():  # 使用交易保證資料完整性。
    #             serializer.save()  # 儲存資料到資料庫。
    #         return JsonResponse(serializer.data)  # 回傳儲存後的資料。
    #     except Exception as e:  # 捕捉例外。
    #         return JsonResponse({'error': str(e)})  # 回傳錯誤訊息。