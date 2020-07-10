from django.db import models

# Create your models here.


class User(models.Model):
    citys = (
        ('BeiJing', '北京'),
        ('ChangChun', '长春'),
        ('ChangSha', '长沙'),
        ('ChengDu', '成都'),
        ('ChongQing', '重庆'),
        ('FuZhou', '福州'),
        ('GuangZhou', '广州'),
        ('GuiYang', '贵阳'),
        ('HaErBin', '哈尔滨'),
        ('HaiKou', '海口'),
        ('HangZhou', '杭州'),
        ('HeFei', '合肥'),
        ('HongKong', '香港'),
        ('HuHeHaoTe', '呼和浩特'),
        ('JiNan', '济南'),
        ('KunMing', '昆明'),
        ('LanZhou', '兰州'),
        ('LaSa', '拉萨'),
        ('Macau', '澳门'),
        ('NanChang', '南昌'),
        ('NanJing', '南京'),
        ('NanNing', '南宁'),
        ('ShangHai', '上海'),
        ('ShenYang', '沈阳'),
        ('ShiJiaZhuang', '石家庄'),
        ('TaiYuan', '太原'),
        ('TianJin' ,'天津'),
        ('WuHan', '武汉'),
        ('WuLuMuQi', '乌鲁木齐'),
        ('XiAn', '西安'),
        ('XiNing', '西宁'),
        ('YinChuan', '银川'),
        ('ZhengZhou', '郑州'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=32, choices=citys, default='北京')
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

