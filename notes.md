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

# 10. 部署
## 10.1 创建Git版本库
使用git管理项目，进入djangogirls文件夹运行以下命令：

    git init

Git会追踪这个目录下所有文件和文件夹的更改，但是有一些文件我们希望Git忽略它。为此，我们可以在项目根目录下创建一个名为.gitignore的文件。

    *.pyc
    __pycache__
    myvenv
    db.sqlite3
    .DS_Store
    .vscode

在执行git操作之前，最好使用git status命令查看一下当前的状态。

    git status

最后保存所有的更改，并提交到git仓库。

    git add --all .
    git commit -m "My Django Girls app, first commit"

## 10.2 推送代码到GitHub上
在GitHub.com网站创建一个新的仓库，命名为"my-first-blog"。保持"initialise with a README“复选框未选中状态，.gitignore选项为无，让License设置为无。

拷贝仓库克隆URL，然后我们需要把电脑上的Git仓库和GitHub上的关联起来。

    $ git remote add origin https://github.com/<your-github-username>/my-first-blog.git
    $ git push -u origin master

**注意**： 如果在GitHub创建仓库时选中了生成README文件，需要先执行下面的命令：

    git pull --rebase origin master

执行这个命令后会先将GitHub上的仓库先同步到本地，然后才能将本地仓库上传到GitHub。

## 10.3 在PythonAnywhere设置我们的博客

### 1. 在PythonAnywhere注册一个"Beginner"账户。
### 2. 在PythonAnywhere上拉取我们的代码
    
注册完PythonAnywhere，会赚到Dashboard页面，然后选择Consoles下的Bash启动Bash控制台。通过创建一个我们仓库的"Clone"以便从GitHub上拉取代码到PythonAnywhere。在PythonAnywhere控制台输入以下命令：

    $ git clone https://github.com/<your-github-username>/my-first-blog.git

这将会拉取一份你的代码副本到PythonAnywhere上。

### 3. 在PythonAnywhere上创建virtualenv
在Bash控制台下，键入：

    $ cd my-first-blog
    $ virtualenv --python=python3.6 myvenv
    $ source myvenv/bin/activate
    (mvenv) $  pip install django whitenoise

### 4. 收集静态文件
什么是"whitenoise"白噪音？ 它是用来服务所谓的“static files”静态文件的工具。 静态文件是很少改动或者并非可运行的程序代码的那些文件，比如 HTML 或 CSS 文件。 在我们的计算机上，它们以不同的方式工作，我们需要比如“whitenoise”这样的工具来为其服务。

暂且我们只需要在服务器上运行一个额外的命令，就是 collectstatic。 它告诉 Django 去收集服务器上所有需要的静态文件。 就眼下来说主要是使admin管理界面看起来更漂亮的文件。

    (mvenv) $ python manage.py collectstatic

### 5. 在 PythonAnywhere 上创建数据库
服务器与你自己的计算机不同的另外一点是：它使用不同的数据库。因此用户账户以及文章和你电脑上的可能会有不同。

我们可以像在自己的计算机上一样在服务器上初始化数据库，使用 migrate 以及 createsuperuser：

    (mvenv) $ python manage.py migrate
    (mvenv) $ python manage.py createsuperuser

### 6. 将我们的博客发布为一个网络应用程序
现在我们的代码已在PythonAnywhere上，我们的 virtualenv 已经准备好，静态文件已收集，数据库已初始化。我们准备好发布网络应用程序！

通过点击 logo 返回到 PythonAnywhere Dashboard，然后点击 Web 选项卡。最终，点 Add a new web app.

在确认你的域名之后，选择对话框中 manual configuration (注 不是 "Django" 选项) ： 下一步选择 Python 3.6，然后点击 Next 以完成该向导。

### 7. 设置virtualenv
回到PythonAnywhere 上你的Web 应用程序的配置屏，那个页面是每次你想修改服务器上你的应用程序时候要去的页面。

在 “Virtualenv” 一节，点击红色文字 “Enter the path to a virtualenv"，然后键入： /home/< your-username >/my-first-blog/myvenv/。 前进之前，先点击有复选框的蓝色框以保存路径。

### 8. 配置WSGI文件
Django 使用 “WSGI 协议”，它是用来服务 Python 网站的一个标准。PythonAnywhere 支持这个标准。 PythonAnywhere 识别我们 Django 博客的方式是通过配置 WSGI 配置文件。

在"Code"部分中点击“WSGI configuration file” 链接，然后跳转到一个编辑器。

删除所有的内容并用以下内容替换：

    import os
    import sys

    path = '/home/<your-username>/my-first-blog'  # use your own username here
    if path not in sys.path:
        sys.path.append(path)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(get_wsgi_application())

这个文件的作用是告诉 PythonAnywhere 我们的Web应用程序在什么位置，Django 设置文件的名字是什么。它也设置 "whitenoise" 静态文件工具。

点击 Save 然后返回到 Web 选项卡。

一切搞定！点击大大的绿色 Reload 按钮然后你将会看到你的应用程序。页面的顶部可以看到它的链接。

### 9. 调试
如果你在访问你的网站时候看到一个错误，首先要去 error log 中找一些调试信息。 你可以在 PythonAnywhere Web 选项卡 中发现它的链接。 检查那里是否有任何错误信息，底部是最新的信息。

**注意**：如果出现类似下面的错误：
    
    Invalid HTTP_HOST header: 'tigermiao.pythonanywhere.com'. You may need to add 'tigermiao.pythonanywhere.com' to ALLOWED_HOSTS.

需要修改项目的settings.py文件，设置ALLOWED_HOSTS如下：

    ALLOWED_HOSTS = ['*']

# 11. Django urls
当用户打开一个 URL 时，你的应用程序才知道应该展现什么内容。 在 Django 中，我们使用一种叫做 URLconf （URL 配置）的机制 。 URLconf 是一套模式，Django 会用它来把 URL 匹配成相对应的 View。

## 11.1 URL 在 Django 中如何工作
打开mysite/urls.py文件：

    from django.contrib import admin
    from django.urls import path

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]

这表示对于每一个以 admin 开头的 URL，Django 都会找到一个相对应的 view。

## 11.2 首页url
我们想用'http://127.0.0.1:8000/' 作为博客的首页，并展示一个帖子列表。

为了保持mysite/urls.py文件简洁，所以我们从 blog 应用导出 urls 到主 mysite/urls.py 文件。

编辑mystie/urls.py文件：

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('blog.urls', namespace='blog')),
    ]

现在，Django 会把访问 'http://127.0.0.1:8000/' 的请求转到 blog.urls，并看看那里面有没有进一步的指示。

## 11.3 blog.urls
在应用blog中创建文件blog/urls.py：

    from django.urls import path, include
    from . import views

    app_name = 'blog'

    urlpatterns = [
        path('', views.post_list, name='post_lists'),
    ]

首先把Django的方法以及blog应用的全部views导入进来。然后，我们可以加入第一个URL模式。我们现在分配了一个叫做 post_list 的 view 到首页的URL上，即将post_list匹配到空字符串。因为在Django的URL解析器中，'http://127.0.0.1:8000' 并不是URL解析的一部分，即只有 'http://127.0.0.1:8000' 后面的部分会被解析。如果后面的部分为空，即是空字符被解析。这个模式告诉Django，如果有人访问 'http://127.0.0.1:8000' 地址，那么 views.post_list 是这个请求该去的地方。

最后的部分，namespace='post_list' 是 URL 的名字，用来唯一标识对应的 view。 它可以跟 view 的名字一样，也可以完全不一样。 在项目后面的开发中，我们将会使用命名的 URL ，所以在应用中为每一个 URL 命名是重要的。

# 12. Django视图
视图都被置放在views.py文件中。我们将加入我们自己的views到blog/views.py文件。

## 12.1 blog/views.py
打开这个文件，然后然后编写代码：

    from django.shortcuts import render

    def post_list(request):
        return render(request, 'blog/post_list.html', {})
    
我们创建了一个名为post_list的函数，它接受request作为参数，并返回用render方法渲染模板 blog/post_list.html 而得到的结果。

# 13. 创建一个模板
模板保存在 blog/templates/blog 目录中。然后在目录中创建一个叫做 post_list.html 的文件。

## 13.1 自定义模板
下面是模板的一个完整实例：

    <html>
        <head>
            <title>Django Girls blog</title>
        </head>
        <body>
            <div>
                <h1><a href="">Django Girls Blog</a></h1>
            </div>

            <div>
                <p>published: 14.06.2014, 12:14</p>
                <h2><a href="">My first post</a></h2>
                <p>Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
            </div>

            <div>
                <p>published: 14.06.2014, 12:14</p>
                <h2><a href="">My second post</a></h2>
                <p>Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut f.</p>
            </div>
        </body>
    </html>

## 13.2 部署

### 13.2.1 提交并推送代码到GitHub
首先，让我们看看上次部署之后什么文件改变了：

    git status

然后，告诉git包括此目录内所有更改：

    git add --all .

在我们上传所有文件前，让我们检查git将上传什么：

    git status

然后提交：

    git commit -m "Changed the HTML for the site."

做完这些，我们上传改动到GitHub：

    git push

### 13.2.2 把新代码来到PythonAnywhere

* 打开 PythonAnywhere consoles page 并转到你的 Bash console（或启动一个新的）。然后，运行：

    cd ~/my-first-blog
    source myvenv/bin/activate
    git pull
    python manage.py collectstatic

* 最后，跳到 Web tab 并点击对应你的 Web 应用程序的 Reload 。

# 14. QuerySets（查询集）
## 14.1 QuerySet是什么？
从本质上说，QuerySet是给定模型的对象列表。QuerySet允许你从数据库中读取数据，对其进行筛选以及排序。

## 14.2 Django shell
在本地终端输入这个命令：

    python manage.py shell

## 14.3 所有对象
在Django shell中输入下面的命令：

    from blog.models import Post

    Post.objects.all()

## 14.4 创建对象
创建一个新的Post对象的方法：

    from django.contrib.auth.models import User

    User.objects.all()
    me = User.objects.get(username='admin')
    Post.objects.create(author=me, title='Sample title', text="Test')
    Post.objects.all()

## 14.5 筛选对象
QuerySets的很多一部分功能是对它们进行筛选。我们将使用filter，而不是all方法。我们需要将筛选条件作为方法的参数。比如，我们要查询指定作者的博客：

    Post.objects.filter(author=me)

或者我们想查询指定title的所有帖子：

    Post.objects.filter(title__contains='title')

**注** title与contains之间有两个下划线字符(_)。Django的ORM使用此语法来分割字段名称（"title"）和操作或筛选器（"contains"）。

也可以获取一个所有已发布文章的列表。我们通过筛选所有含 published_date 为过去时间的文章来实现这个目的：

    from django.utils import timezone

    post = Post.objects.get(title="Sample title")
    post.publish()
    Post.objects.filter(published_date__lte=timezone.now())

## 14.6 对象排序
QuerySet 还允许排序结果集对象的列表。比如：按 create_date 字段排序：

    Post.objects.order_by('created_date')

我们也可以在开头添加 - 来反向排序：

    Post.objects.order_by('-created_date')

## 14.7 链式 QuerySets
你可以通过链式调用连续组合QuerySets

    Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

# 15. 模板中的动态数据
views的作用是连接模型和模板。在视图函数 post_list 中我们获取我们想要显示的模型，并将它们传递到模板中去。所以基本上在视图中，我们决定什么（模型）将显示在模板中。

现在是我们必须导入我们已经写在 models.py 里的模型的时候了。

    from django.shortcuts import render
    from django.utils import timezone
    from .models import Post

    def post_list(request):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})

from 后面的点号意味着 当前目录 或 当前的应用程序。 因为 views.py 和 models.py 是在同一目录中，我们只需要使用 . 和 文件的名称（无 .py) 。 然后我们导入模型（Post).

现在我们对已经发表并进行由 published_date排序的博客列表感兴趣。我们创建了QuerySet查询集变量：posts。并在最后将posts查询集传递给模板。

render函数包含三个参数：request（请求）和模板文件 'blog/post_list.html'。最后一个参数是一个字典，字典中包含模板需要的参数，我们将posts查询集作为参数传给了模板。

# 16. Django模板
## 16.1 什么是模板标签？
Django模板标签允许我们将Python之类的内容翻译成HTML。
## 16.2 展现文章列表模板
为了用模板标签在HTML中显示变量，我们使用两个大括号，并将变量包含在里面：

    {{ posts }}

修改模板文件 blog/templates/blog/post_list.html，并使用模板标签 {{ posts }}:

    <div>
        <h1><a href="/">Django Girls Blog</a></h1>
    </div>

    {% for post in posts %}
        <div>
            <p>published: {{ post.published_date }}</p>
            <h1><a href="">{{ post.title }}</a></h1>
            <p>{{ post.text|linebreaksbr }}</p>
        </div>
    {% endfor %}

我们使用循环去遍历对象列表，所有的在{% for %} 和 {% endfor %} 之间的内容将会被Django对象列表中的每个对象所代替。我们还使用了 {{ post.title }} 和 {{ post.text }} 去访问Post模型中的属性。此外，|linebreaksbr是一个过滤器，使得行间隔变成段落。

## 16.3 部署
再次部署到PythonAnywhere。部署步骤如下：

* 首先，将代码上传到GitHub

    git status
    git add --all .
    git status
    git commit -m "Modified templates to display posts from database."
    git push

* 然后，重新登录PythonAnywhere并进入Bash控制台，并运行：

    cd my-first-blog
    git pull

* 最后，我们返回 Web tab 重新加载我们的应用程序， 此时我们应该可以看到更新后的程序运行情况了。