from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from io import BytesIO
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import FileUpload
from .utils import decrypt_file

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import RegisterSerializer, FileUploadSerializer
from .models import FileUpload
from django.core.files.base import ContentFile
from .utils import encrypt_file, decrypt_file

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        uploaded_file = request.FILES['file']
        encrypted_data = encrypt_file(uploaded_file.read())
        encrypted_file = ContentFile(encrypted_data, name=uploaded_file.name + '.enc')

        file_record = FileUpload.objects.create(
            user=request.user,
            file_name=uploaded_file.name,
            encrypted_file=encrypted_file,
            size=uploaded_file.size
        )

        return Response(FileUploadSerializer(file_record).data, status=201)

class ListFilesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        files = FileUpload.objects.filter(user=request.user)
        return Response(FileUploadSerializer(files, many=True).data)

# class DownloadFileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             file_obj = FileUpload.objects.get(id=pk, user=request.user)
#         except FileUpload.DoesNotExist:
#             return HttpResponse("File not found", status=404)

#         # Read and decrypt the file
#         encrypted_content = file_obj.encrypted_file.read()
#         decrypted_content = decrypt_file(encrypted_content)

#         # Serve as downloadable response
#         file_stream = BytesIO(decrypted_content)
#         response = FileResponse(file_stream, as_attachment=True, filename=file_obj.file_name)
#         return response

from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from io import BytesIO
from .models import FileUpload
from .utils import decrypt_file
class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]  # to accept JSON body

    def post(self, request):
        file_id = request.data.get("file_id")

        if not file_id:
            return JsonResponse({"error": "Missing file ID"}, status=400)

        try:
            file_obj = FileUpload.objects.get(id=file_id, user=request.user)
        except FileUpload.DoesNotExist:
            return JsonResponse({"error": "File not found"}, status=404)

        encrypted_content = file_obj.encrypted_file.read()
        decrypted_content = decrypt_file(encrypted_content)

        file_stream = BytesIO(decrypted_content)
        return FileResponse(file_stream, as_attachment=True, filename=file_obj.file_name)