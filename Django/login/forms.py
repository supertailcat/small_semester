from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
	username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
	password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
		attrs={'class': 'form-control', "placeholder": "Password"}))
	captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
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
		('TianJin', '天津'),
		('WuHan', '武汉'),
		('WuLuMuQi', '乌鲁木齐'),
		('XiAn', '西安'),
		('XiNing', '西宁'),
		('YinChuan', '银川'),
		('ZhengZhou', '郑州'),
	)
	username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label="确认密码", max_length=256,
								widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
	city = forms.ChoiceField(label='城市', choices=citys)
	captcha = CaptchaField(label='验证码')
