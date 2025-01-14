_Z='menu_2'
_Y='menu_1'
_X='menu_active'
_W='menu_class_2'
_V='menu_class_1'
_U='google calendar'
_T='product'
_S='why us'
_R='sub title'
_Q='priority'
_P='frontend'
_O='Middle'
_N='posts_updated'
_M='post_deleted'
_L='name'
_K='order_item'
_J='link'
_I=None
_H='max'
_G='photo'
_F='site'
_E='content'
_D='extends'
_C='title'
_B=False
_A=True
import math,os,string
from bs4 import BeautifulSoup as bs
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django_cryptography.fields import encrypt
from jsonfield import JSONField
from menu.models import Menu
from parler.models import TranslatableModel,TranslatedFields
from uuslug import uuslug
from core.models import ModelList,ModelListSetting,Photo
from django_authbox.common import get_site_id
from .abstract import BaseAbstractModel
User=get_user_model()
exposed_request=_I
class Logo(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);name=models.CharField(_('logo name'),max_length=100);photo=GenericRelation(Photo)
	class Meta:verbose_name=_('logo');verbose_name_plural=_('logos')
	def __str__(A):return f"{A.name}"
class Favicon(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);name=models.CharField(_('favicon name'),max_length=100);photo=GenericRelation(Photo)
	class Meta:verbose_name=_('favicon');verbose_name_plural=_('favicons')
	def __str__(A):return f"{A.name}"
class OptStatusPublish(models.IntegerChoices):DRAFT=1,_('Draft');PUBLISHED=2,_('Published')
class OptSocialMediaKinds(models.IntegerChoices):FACEBOOK=1,_('Facebook');TWITTER=2,_('Twitter');PINTEREST=3,_('Pinterest');YOUTUBE=4,_('Youtube');INSTAGRAM=5,_('Instagram')
class OptPriority(models.IntegerChoices):HIGH=1,_('High');MIDDLE=2,_(_O);LOW=3,_('Low')
def word_count(text):A=bs(text,'html.parser');B=A.get_text();return sum([A.strip(string.punctuation).isalpha()for A in B.split()])
def reading_time(wordcount):B=200;C,D=math.modf(wordcount/B);E=1 if C*60>=30 else 0;A=D+E;return 1 if A<=0 else A
class Tags(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);translations=TranslatedFields(name=models.CharField(_('tags name'),max_length=50));slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('tag');verbose_name_plural=_('tags')
	def __str__(A):return f"{A.name}"
	def save(A,*B,**C):A.slug=uuslug(A.name,instance=A,max_length=50);super().save(*(B),**C)
class Categories(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);translations=TranslatedFields(name=models.CharField(_('categories name'),max_length=50));slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('category');verbose_name_plural=_('categories')
	def __str__(A):return f"{A.name}"
	def save(A,*B,**C):A.slug=uuslug(A.name,instance=A,max_length=50);super().save(*(B),**C)
class BaseContentModel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);view_count=models.PositiveIntegerField(_('view count'),default=0,editable=_B);share_count=models.PositiveIntegerField(_('share count'),default=0,editable=_B);slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A,editable=_B);photo=GenericRelation(Photo,verbose_name=_(_G));tags=models.ManyToManyField(Tags,verbose_name=_('tags'));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:app_label=_P;abstract=_A
class Announcement(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));categories=models.ForeignKey(Categories,on_delete=models.PROTECT);word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);priority=models.SmallIntegerField(choices=OptPriority.choices,default=OptPriority.LOW,verbose_name=_(_Q))
	class Meta:verbose_name=_('announcement');verbose_name_plural=_('announcements')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class News(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));categories=models.ForeignKey(Categories,on_delete=models.PROTECT);word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B)
	class Meta:verbose_name=_('news');verbose_name_plural=_('news')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class Article(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));categories=models.ForeignKey(Categories,on_delete=models.PROTECT);word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);is_header_text=models.BooleanField(default=_B)
	class Meta:verbose_name=_('article');verbose_name_plural=_('articles')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class Events(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)),location=encrypt(models.CharField(_('location'),max_length=255,null=_A,blank=_A)));categories=models.ForeignKey(Categories,on_delete=models.PROTECT);word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);date=models.DateField(_('date'));time=models.TimeField(_('time'))
	class Meta:verbose_name=_('event');verbose_name_plural=_('events')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class SlideShow(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=GenericRelation(Photo);translations=TranslatedFields(title=models.CharField(_(_C),max_length=500),sub_title=models.CharField(_(_R),max_length=500,null=_A,blank=_A),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('slide show');verbose_name_plural=_('slides show')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);super().save(*(B),**C)
class DailyAlert(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);translations=TranslatedFields(alert=encrypt(models.CharField(_('alert'),max_length=500)));link=models.CharField(_(_J),max_length=255,null=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('daily alert');verbose_name_plural=_('daily alerts')
	def __str__(A):return f"{A.alert}"
class WhyUs(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);icon=models.CharField(_('icon'),max_length=100);translations=TranslatedFields(title=models.CharField(_(_C),max_length=100),description=models.CharField(_('description'),max_length=500));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_(_S);verbose_name_plural=_(_S)
	def __str__(A):return f"{A.icon}"
class Greeting(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=GenericRelation(Photo,verbose_name=_(_G));translations=TranslatedFields(title=models.CharField(_(_C),max_length=500),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)),name=encrypt(models.CharField(_('greeting name'),max_length=255,null=_A,blank=_A)),designation=encrypt(models.CharField(_('designation'),max_length=255,null=_A,blank=_A)));slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A,editable=_B);view_count=models.PositiveIntegerField(default=0,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('greeting');verbose_name_plural=_('greetings')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);super().save(*(B),**C)
class Pages(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));menu=models.ForeignKey(Menu,on_delete=models.PROTECT,verbose_name='Access From Menu',blank=_A);word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B)
	class Meta:verbose_name=_('page');verbose_name_plural=_('pages')
	def __str__(A):return A.title
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class SocialMedia(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));kind=models.SmallIntegerField(choices=OptSocialMediaKinds.choices,verbose_name=_('kind'));link=encrypt(models.URLField(_(_J),max_length=255));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.site.name} - {A.get_kind_display()}"
class BaseGalleryModel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);view_count=models.PositiveIntegerField(default=0,editable=_B);slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:app_label=_P;abstract=_A
class PhotoGallery(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_G))
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);super().save(*(B),**C)
class Fasilities(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_G),null=_A,blank=_A)
	def __str__(A):return f"{A.title}"
	def save(A,*C,**D):
		A.slug=uuslug(A.title,instance=A,max_length=255)
		if A.order_item==0:
			B=Fasilities.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max(_K))
			if B:
				if not B[_H]is _I:A.order_item=B[_H]+1
		super().save(*(C),**D)
class Offers(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_G),null=_A,blank=_A)
	def __str__(A):return f"{A.title}"
	def save(A,*C,**D):
		A.slug=uuslug(A.title,instance=A,max_length=255)
		if A.order_item==0:
			B=Offers.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max(_K))
			if B:
				if not B[_H]is _I:A.order_item=B[_H]+1
		super().save(*(C),**D)
class HowItWorks(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	icon=models.CharField(_('icon'),max_length=100,null=_A,blank=_A);translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=100)),content=encrypt(models.CharField(_(_E),max_length=500)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_G),null=_A,blank=_A)
	def __str__(A):return f"{A.title}"
	def save(A,*C,**D):
		A.slug=uuslug(A.title,instance=A,max_length=255)
		if A.order_item==0:
			B=HowItWorks.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max(_K))
			if B:
				if not B[_H]is _I:A.order_item=B[_H]+1
		super().save(*(C),**D)
class AboutUs(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(sub_title=encrypt(models.CharField(_(_R),max_length=100)),title=encrypt(models.CharField(_(_C),max_length=100)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));photo=GenericRelation(Photo,verbose_name=_(_G),null=_A,blank=_A)
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);super().save(*(B),**C)
class Product(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(name=encrypt(models.CharField(_(_L),max_length=100)),title=encrypt(models.CharField(_(_C),max_length=100)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);icon=models.CharField(max_length=100,null=_A,blank=_A);photo=GenericRelation(Photo,verbose_name=_(_G),null=_A,blank=_A)
	def __str__(A):return f"{A.name}"
	def save(A,*C,**D):
		A.slug=uuslug(A.name,instance=A,max_length=255)
		if A.order_item==0:
			B=Product.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max(_K))
			if B:
				if not B[_H]is _I:A.order_item=B[_H]+1
		super().save(*(C),**D)
class Cart(BaseAbstractModel):
	product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name=_(_T));qty=models.PositiveIntegerField(default=1,blank=_A,editable=_B);site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.product.name}"
class Purchasing(BaseAbstractModel):
	product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name=_(_T));qty=models.PositiveIntegerField(default=1,blank=_A,editable=_B);site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.product.name}"
def save_embed_video(embed):
	E='src';D=0;A='';F=embed.split(' ');B=_B
	for G in F:
		if B:break
		H=G.split('=');B=_B
		for C in H:
			if not B and C.lower()==E:B=_A
			if B and C.lower()!=E:
				if D==0:A+=C;D+=1
				else:A+='='+C
				print(A)
	if A.find('watch')<=0:A=A.replace('"','');A=A.replace('&quot;','');return A
	else:return _I
class VideoGallery(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)));embed=CKEditor5Field(_('embed'),blank=_A,null=_A,config_name=_D);embed_video=models.URLField(blank=_A,null=_A);photo=GenericRelation(Photo,verbose_name=_(_G))
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);A.embed_video=save_embed_video(A.embed);super().save(*(B),**C)
class RelatedLink(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,blank=_A,verbose_name=_(_F));link=encrypt(models.URLField(_(_J),max_length=255));translations=TranslatedFields(name=encrypt(models.CharField(_(_L),max_length=150)));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.name}"
class Document(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);file_path_doc=models.FileField(verbose_name=_('file path Document'));translations=TranslatedFields(name=encrypt(models.CharField(_(_L),max_length=150)),content=encrypt(CKEditor5Field(_(_E),blank=_A,null=_A,config_name=_D)));categories=models.ForeignKey(Categories,on_delete=models.PROTECT);word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);size=models.BigIntegerField(_('size'),null=_A,blank=_A,default=0,editable=_B);hits=models.IntegerField(_('hits'),null=_A,blank=_A,default=0,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.name}"
	def save(A,*B,**C):A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class Popup(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)));link=encrypt(models.URLField(_(_J),max_length=255,null=_A,blank=_A));photo=GenericRelation(Photo,verbose_name=_(_G));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.title}"
class Banner(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=GenericRelation(Photo,verbose_name=_(_G));link=models.URLField(max_length=255,null=_A,blank=_A);priority=models.SmallIntegerField(choices=OptPriority.choices,default=OptPriority.LOW,verbose_name=_(_Q));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):
		B=''
		if A.priority==1:B='High'
		elif A.priority==2:B=_O
		elif A.priority==3:B='Low'
		B=f"{B} [{A.site.id}] {A.site} {A.link}";return B
class Location(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=500)));embed=CKEditor5Field(_('embed'),blank=_A,null=_A,config_name=_D)
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):A.slug=uuslug(A.title,instance=A,max_length=255);super().save(*(B),**C)
def get_upload_path(instance,filename):return os.path.join('credentials',f"{instance.site_id}_{filename}")
class GoogleCalendar(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);cal_name=models.CharField(_('google calendar ID'),max_length=100);file_path_doc=models.FileField(verbose_name=_('google calendar credentials path'),upload_to=get_upload_path,blank=_A,null=_A);is_default=models.BooleanField(default=_B)
	class Meta:verbose_name=_(_U);verbose_name_plural=_('google calendars')
	def __str__(A):return A.cal_name
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);super().save(*(B),**C)
class GoogleCalendarDetail(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);google_calendar=models.ForeignKey(GoogleCalendar,on_delete=models.CASCADE,verbose_name=_(_U));cal_year=models.PositiveIntegerField(default=2023,blank=_A,editable=_B);cal_month=models.PositiveIntegerField(default=2023,blank=_A,editable=_B);cal_json=JSONField(null=_A,blank=_A)
	class Meta:verbose_name=_('google calendar detail');verbose_name_plural=_('google calendars detail')
	def __str__(A):return f"{A.cal_month}/{A.cal_year}"
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);super().save(*(B),**C)
@receiver(models.signals.post_delete,sender=Document)
@receiver(models.signals.post_delete,sender=GoogleCalendar)
def auto_delete_file_on_delete(sender,instance,**B):
	A=instance
	if A.file_path_doc:
		if os.path.isfile(A.file_path_doc.path):os.remove(A.file_path_doc.path)
@receiver(models.signals.pre_save,sender=Document)
@receiver(models.signals.pre_save,sender=GoogleCalendar)
def auto_delete_file_on_change(sender,instance,**E):
	C=sender;A=instance
	if not A.pk:return _B
	try:B=C.objects.get(pk=A.pk).file_path_doc
	except C.DoesNotExist:return _B
	D=A.file_path_doc
	if not B==D:
		if os.path.isfile(B.path):os.remove(B.path)
@receiver(post_delete,sender=Menu,dispatch_uid=_M)
@receiver(post_delete,sender=ModelList,dispatch_uid=_M)
@receiver(post_delete,sender=ModelListSetting,dispatch_uid=_M)
def menu_post_delete_handler(sender,**B):
	A=get_site_id(exposed_request)
	if A>0:print('clear cache delete',A);cache.delete(_V,version=A);cache.delete(_W,version=A);cache.delete(_X,version=A);cache.delete(_Y,version=A);cache.delete(_Z,version=A)
@receiver(post_save,sender=Menu,dispatch_uid=_N)
@receiver(post_save,sender=ModelList,dispatch_uid=_N)
@receiver(post_save,sender=ModelListSetting,dispatch_uid=_N)
def menu_post_save_handler(sender,**B):
	A=get_site_id(exposed_request)
	if A>0:print('clear cache update',A);cache.delete(_V,version=A);cache.delete(_W,version=A);cache.delete(_X,version=A);cache.delete(_Y,version=A);cache.delete(_Z,version=A)