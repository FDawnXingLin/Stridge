# Stridge
Stridge是一个基于静态文件的短链接服务应用。它可以与Github Pages等网页托管服务搭配使用，在不需要动态服务器的情况下实现可自定义域名的链接缩短服务。
## 实现
Stridge的核心功能是一个页面渲染器，在用户通过CLI添加网址后，页面渲染器会为每条对应关系渲染一个页面。这些页面被部署到静态文件托管服务之后，用户就可以通过访问短网址来跳转到原始地址。
## 安装
`git clone --depth 1 git@github.com:FDawnXingLin/Stridge.git`
## 使用
在第一次执行任何一个命令时，Stridge会自动初始化。
### 添加URL
`stridge.py add <url> [--symbol <symbol>]` 

add命令可以添加一条对应关系到数据文件中，其中<url>为必须项，是你所想要为其生成短网址的原始网址。而[symbol]则是短网址的后缀，为可选项。如果不指定[symbol]，系统将会自动生成一个。
### 删除URL
`stridge.py remove <symbol>`

remove命令可以删除一条数据文件中的对应关系，其中<symbol>为必须项，是你所想要移除的短网址的<symbol>。
### 生成页面
`stridge.py generate`

generate命令可以根据数据文件渲染出静态文件，并将其输出到指定文件夹。在输出之前，目标文件夹会被清空。
### 清空输出
`stridge.py clean`

clean命令可以手动清空输出文件夹而不执行其他操作。
### 程序信息
`stridge.py version`

version命令将会输出程序的版本号等元信息。
## 部署
Stridge所产生的静态文件可以部署在任何静态服务器或者Pages托管服务上。而且你可以根据自己的情况选择两种部署方式。
### 直接部署静态文件
默认情况下，程序输出的静态文件在dist文件夹中，你可以直接上传文件夹中的内容，这一般适用于传统的静态服务器，可以与FTP搭配使用。在后续版本中将进行这方面功能的对接。
### 部署源文件，由托管服务构建
用户可以通过Git将源数据提交到仓库，再通过各Pages服务持续构建静态页面再进行部署。

注意，为了保证仓库的整洁性，我在.gitignore文件中忽略了模板文件、数据文件、输出文件夹这些可以自动生成的文件，但是如果你想将其部署到Pages服务上，模板文件和数据文件都是必要的，所以你需要自定义.gitignore文件，移除这两项。（如果你没有自定义模板文件的话，也可以不上传模板文件，而是让系统自动生成）除此之外，如果你自定义了目录名称和文件名称，你也要进行相应的修改。如果你想加速上传和构建速度的话，你也可以仅上传主程序文件和数据文件。
一个泛用的.gitignore文件可能是：

```
LICENSE
README.md
template.html
dist
```
## 自定义
Stridge提供了很多可以自定义的项目来满足你的需求。这些配置项都是stridge.py中的变量。
### template_file
模板文件的文件名，默认为template.html。可以通过更改此项在不同模板中切换。
### default_template
默认的模板文件内容，当目录下指定的模板文件不存在时，系统将以此内容创建一个模板文件。
### data_file
数据文件的文件名，默认为data.yaml。可以根据用户的喜好来自行更改。
### default_data
默认的数据文件内容，默认为空，当目录下指定的数据文件不存在时，系统将以此内容创建一个数据文件。
### domain
短链接的域名。实际上短链接的域名取决于与静态文件托管服务的域名，这里的设置项只是为了在添加链接时可以直观的输出短网址。