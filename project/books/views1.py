import os

from rest_framework import permissions, mixins, serializers
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from books.permissions import IsOwner
from books.serializers import BookSerializer, BookCreateSerializer
from books.utils import CreateDiffrentMixin
from service.book_config import BOOK_STORE, MAX_BOOKS_SIZE

import logging
from books.tasks import send_book_creation_email
logger = logging.getLogger(__name__)
# Create your views here.

class BookViewSet(CreateDiffrentMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    create_output_serializer = BookSerializer

    def perform_create(self, serializer):
#        logger.debug(f"Received file with size: {book_text.size}")
        logger.info(f"Boojjjjjjjjjkkkkk")
        book_text = serializer.validated_data.pop('text')
        logger.debug(f"Received file with size: {book_text.size}")
        if book_text.size > MAX_BOOKS_SIZE:
            raise serializers.ValidationError("Book is too big")
        if book_text.content_type != 'text/plain':
            raise serializers.ValidationError("File is not a text")
        instance = serializer.save(owner=self.request.user)
        send_book_creation_email.delay(self.request.user.email, instance.title)
        logger.info(f"Book created with UID: {instance.uid}")
        description_filename = os.path.join(BOOK_STORE, f"{instance.uid}.txt")
        print('OK')
        with open(description_filename, 'wb+') as f:
            for chunk in book_text.chunks():
                f.write(chunk)
        print('OK')

    def get_queryset(self):
#        return Book.objects.filter(owner=self.request.user)
        return Book.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return BookCreateSerializer

        return BookSerializer
