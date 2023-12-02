"""
Раздел: Managin files (Управление файлами).


По умолчанию файлы хранятся локально, используя настройки MEDIA_ROOT и MEDIA_URL.

Сохранение файла на диске:
from pathlib import Path
from django.core.files import File
path = Path('/some/external/specs.pdf')
car = Car.objects.get(name='Chery')
with path.open(mode='rb') as f:
    car.specs = File(f, name=path.name)
    car.save()


Открытие изображения:

from PIL import Image
car = Car.objects.get(name='Chery')
car.photo.width
car.photo.height
image = Image.open(car.photo)
car.photo.open()
image = Image.open(car.photo)
image


Обьект File

from django.core.files import File
f = open(/path/to/hello.world', 'w')
myfile = File(f)

with open('/path/to/hello.world', 'w') as f:
    myfile = File(f)
    myfile.write('Hello world')

myfile.closed
f.closed


По умолчанию файловое хранилище:
django.core.files.storage.FileSystemStorage из STORAGES.


"""