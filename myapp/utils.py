from django.db import models
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

class ObjectWithFileField(models.Model):
    image = models.FileField(upload_to="uploads/icon", null= True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    
    def get_image_from_url(self, url):
        img_tmp = NamedTemporaryFile(delete=True)
        with urlopen(url) as uo:
            assert uo.status == 200
            img_tmp.write(uo.read())
            img_tmp.flush()
        img = File(img_tmp)
        self.image.save(img_tmp.name, img)
        self.image_url = url

#ユーザのアイコン画像を取得してそのurlを返す関数
def get_avatar_url(a_user):
        if a_user.socialaccount_set.exists():
            return a_user.socialaccount_set.first().get_avatar_url()

