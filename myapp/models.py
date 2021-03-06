from django.db import models
from accounts.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.TextChoices):
    NOVEL = 'novel','文学/小説'
    SOCIETY = 'society','人文/社会'
    CULTURE = 'culture','ノンフィクション/教養'
    TRAVEL = 'travel','地図/旅行ガイド'
    ECONOMY = 'economy','ビジネス/経済'
    HEALTH = 'health','健康/医学'
    IT = 'IT','コンピュータ/IT'
    HOBBY = 'hobby','趣味/スポーツ/実用'
    LIFE = 'life','住まい/暮らし/子育て'
    ART = 'art','アート/エンタメ'
    FOREIGN = 'foreign','洋書'
    PICTURE = 'picture','絵本'
    STUDY = 'study','参考書'
    OTHER = 'other','その他'


class Quality(models.TextChoices):
    NEW = 'new','新品/未使用'
    NO_DAMAGED = 'no_damaged','目立った傷や汚れなし'
    LITTLE_DAMAGED = 'little_damaged','やや傷や汚れあり'
    DAMAGED = 'damaged','傷や汚れあり'
    BAD = 'bad','全体的に状態が悪い'

class Sort(models.TextChoices):
    A_CREATED_TIME = 'a_created_time','新しい順'
    A_PRICE = 'a_price','価格の安い順'
    D_CREATED_TIME = 'd_created_time','古い順'
    D_PRICE = 'd_price','価格の高い順'


class Item(models.Model):
    
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="seller",blank=True
    )

    buyer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="buyer",blank=True,null=True
    )

    image = models.FileField(
        verbose_name="商品画像", upload_to="uploads/item", 
    )

    name = models.CharField(max_length=30)

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        
    )

    quality = models.CharField(
        max_length=20,
        choices=Quality.choices,
    )

    price = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )

    detail = models.TextField(max_length=5000)

    sell_time = models.DateTimeField(auto_now_add=True)

    give_time = models.DateTimeField(blank=True,null=True)

    is_purchased = models.BooleanField(default=False,blank=True)

    is_settle = models.BooleanField(default=False,blank=True)

    is_given = models.BooleanField(default=False,blank=True)

    is_got = models.BooleanField(default=False,blank=True)



    class Meta:
        verbose_name_plural = 'Item'


class Talk(models.Model):
    # メッセージ
    talk = models.CharField(max_length=500)
    # 誰から
    talk_from = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="talk_from"
    )
    # 誰に
    talk_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="talk_to")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)

    talk_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="talk_item"
    )



    class Meta:
        verbose_name_plural = 'Talk'

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)


class Nortify(models.Model):
    #誰に
    notice_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notice_to")
    # トーク画面に行くために
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="talk_with",blank=True,null=True)
    #どの商品に対して
    nortify_item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name="nortify_item")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)
    #内容
    nortify = models.CharField(max_length=100,blank=True,null=True)
    #チェックされたかどうか
    is_checked = models.BooleanField(default=False)

    def set_purchased(self,item,user):
        self.nortify = item.name + "が" + user.username + "さんに購入されました。渡したら、トーク画面の「渡したボタン」を押してください。"

    def set_message(self,user):
        self.nortify = user.username + "さんからメッセージが届きました"

    def set_given(self,user):
        self.nortify = user.username + "さんが商品を渡したようです。受け取ったら、トーク画面の「受け取ったボタン」を押してください。"

    def set_end(self,user):
        self.nortify = user.username + "さんとの取引が終了しました。お疲れ様でした。"

    class Meta:
        verbose_name_plural = 'Nortify'
