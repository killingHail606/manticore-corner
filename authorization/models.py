from PIL import Image
from django.db import models
from django.contrib.auth.models import User


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    email_newsletters = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='profile_images/', default='user/no-avatar.png')

    def __str__(self):
        return self.user.username

    def save_avatar(self, *args, **kwargs):
        if self.picture:
            name_picture = self.picture.__str__()

            im = Image.open(self.picture)
            im_new = crop_max_square(im)
            im_new.save(f'media/profile_images/{name_picture}', quality=95)
            self.picture = f'/profile_images/{name_picture}'
        super(Profile, self).save(*args, **kwargs)