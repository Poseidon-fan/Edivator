from django.db import models


class BaseModel(models.Model):
    """抽象的模型基类，用于定义一些公共的字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        abstract = True  # 声明为抽象模型
        verbose_name = '公共字段表'
        db_table = 'BaseTable'
