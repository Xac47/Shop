from django.db import models


class ManagerCustom(models.Manager):

    def __init__(self, status_product):
        self.status_product = status_product
        super().__init__()

    def get_queryset(self):
        return super().get_queryset().filter(status=self.status_product)
