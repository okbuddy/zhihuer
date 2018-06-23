from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import signing

class User(AbstractUser):
    '''用户模型'''
    gender_choices = (
        ('M', '男'),
        ('F', '女')
        )
    nickname = models.CharField('昵称', max_length=40, null=True, blank=True)
    email = models.EmailField('邮箱')
    gender = models.CharField('性别', choices=gender_choices, max_length=1, default='M')
    address = models.CharField('地址', max_length=100, null=True, blank=True)
    description = models.CharField('个人描述', max_length=400, null=True, blank=True)
    image = models.ImageField('用户头像', upload_to='image/%Y/%m', default='image/default_user.png', null=True, blank=True)
    add_time = models.DateTimeField('加入时间', auto_now_add=True)
    confirmed = models.BooleanField('用户确认', default=False)

    def __str__(self):
        return self.username

    def get_topic_nums(self):
        return self.topic_set.all().count()

    def get_collect_answer_nums(self):
        return self.usercollectanswer_set.all().count()

    def get_follow_question_nums(self):
        return self.userfollowquestion_set.all().count()

    def get_answer_by_followed_nums(self):
        '''获取所有回答的被关注数量'''
        from zhihu.models import UserFollowAnswer
        return UserFollowAnswer.objects.filter(answer__author=self).count()

    def get_answer_by_collected_nums(self):
        '''获取所有回答的被关注数量'''
        from zhihu.models import UserCollectAnswer
        return UserCollectAnswer.objects.filter(answer__author=self).count()

    def generate_confirm_token(self):
        '''生成用户确认签名'''
        token = signing.dumps({'confirm': self.id})
        return token

    def confirm(self, token, max_age=24*60*60):
        '''验证确认签名'''
        try:
            data = signing.loads(token, max_age=max_age)
        except Exception as e:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.save()
        return True
