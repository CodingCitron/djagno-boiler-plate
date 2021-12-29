from django.db import models

# Create your models here.
class Board(models.Model):
    post_id = models.AutoField(primary_key=True, verbose_name='게시글 아이디')
    category = models.CharField(max_length=128, default="기본 게시판", verbose_name='카테고리')
    title = models.CharField(max_length=256, null=True, verbose_name='게시글 제목')
    contents = models.TextField(verbose_name='게시글 내용')
    writer = models.CharField(max_length=32, verbose_name='작성자')
    register_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='등록일')

    class Meta:
        db_table = 'board'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'