# 1. Django安装
## 1.1 虚拟环境
创建新目录djangogirls:
    
    mkdir djangogirls
    cd djangogirs

创建虚拟环境myvenv：

    python3 -m venv myvenv

## 1.2 使用虚拟环境
运行如下命令进入虚拟环境：

    source myvenv/bin/activate

## 1.3 安装Django
在虚拟环境中，使用pip安装Django。

    pip install django

# 2. 创建Django项目
在虚拟环境中运行下面的命令，不要漏掉命令后面的小点（.）：

    django-admin startproject mysite .

符号“.“告诉脚本程序在当前目录下创建Django项目，项目名为mysite。

# 3. 更改设置
修改mystie/settings.py文件更改设置。找到包含TIME_ZONE字段的这行，更改为你所在地区的时区，如：

    TIME_ZONE = ‘Asia/Shanghai'

添加静态文件的路径，在文件的最底部，STATIC_URL条目的下面，添加一行内容为STATIC_ROOT：

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 4. 设置数据库
我们使用默认的sqlite3数据库，这已经在您的mysite/settings.py文件中设置了：

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

要为项目创建一个数据库，需要运行以下命令：

    python manage.py migrate

然后运行命令启动web服务器：

    python manage.py runserver

# 5. Django模型
Django里的模型是一种特殊的对象--它保存在数据库中。

# 6. 创建应用程序
为了创建一个应用程序，我们需要在命令行中执行以下命令：

    python manage.py startapp blog

创建应用程序后，我们还需要告诉Django它应该使用它。在mysite/settings.py文件中，找到INSTALLED_APPS并在它下面添加一行'blog'：

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'blog',
    )

# 7. 创建一个博客文章模型
在blog/models.py文件中，定义所有的Models对象：

    from django.db import models
    from django.utils import timezone


    class Post(models.Model):
        author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
        title = models.CharField(max_length=200)
        text = models.TextField()
        created_date = models.DateTimeField(
                default=timezone.now)
        published_date = models.DateTimeField(
                blank=True, null=True)

        def publish(self):
            self.published_date = timezone.now()
            self.save()

        def __str__(self):
            return self.title

* models.Model表明Post是一个Django模型，所以Django知道它应该被保存在数据库中。
* models.CharField - 这是你如何用为数有限的字符来定义一个文本。
* models.TextField - 这是没有长度限制的长文本。
* models.DateTimeField - 这是日期和时间。
* models.ForeignKey - 这是指向另一个模型的连接。

# 8. 在数据库中为模型创建数据表
最后一步是将新的模型添加到我们的数据库。首先必须让Django知道我们的模型有一些变更：

    python manage.py makemigrations blog

然后让Django为我们准备必须应用到我们数据库的迁移文件：

    python manage.py migrate blog

# 9. Django admin管理后台
## 9.1 创建超级用户

    python manage.py createsuperuser

## 9.2 使用Django admin管理帖子
编辑blog/admin.py文件：

    from django.contrib import admin
    from .models import Post

    admin.site.register(Post)

我们导入了Post模型，为了让我们的模型在admin页面上可见，我们需要使用admin.site.register(Post)来注册模型。

