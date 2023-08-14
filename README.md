<!--suppress HtmlDeprecatedAttribute -->
<h1 align="center">DatingBot</h1>

> An open source telegram bot with which you can find new acquaintances

## :books: Table of Contents

- [Installation](#package-installation)
- [Usage](#rocket-usage)
- [Django](#green_book-django)
- [NudeNet](#see_no_evil-nudenet)
    - [Possible Errors](#goal_net-possible-errors)
- [Contributing](#busts_in_silhouette-contributing)

## 🖍 Used technology

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## :package: Installation

#### First check if you have Python installed

Before installing this DatingBot-project you need to check if you have python\
To check if you have python installed, run this command in your terminal:

```sh
$ python -V
```

If you get an answer like this, it means that `Python` is installed.

```sh
$ Python 3.9.5
```

#### Then clone the DatingBot

```sh
$ git clone https://github.com/DavidRomanovizc/DatingBot.git
```

and create a Virtual Environment

```sh
$ python -m venv venv
```

Activate the virtual environment:

<u>On Windows:</u>

```sh
$ venv\Scripts\activate
```

<u>On macOS and Linux:</u>

```sh
$ source venv/bin/activate
```

and install requirements

```sh
$ pip install -r requirements.txt
```

## :rocket: Usage

First you need to rename the file `.env.dist` to `.env`.\
After that, you need to fill it with data.

| Variable      | Type | Importance | Description                                                                 |
|---------------|------|------------|-----------------------------------------------------------------------------|
| BOT_TOKEN     | str  | True       | Bot token                                                                   |
| ADMINS        | list | True       | list of admins id                                                           |
| SUPPORTS      | list | True       | list of supports id                                                         |
| IP            | str  | True       | ip for other services                                                       |
| TIMEZONE      | str  | True       | your time zone for working with the scheduler                               |
| MODERATE_CHAT | str  | True       | telegram chat where the event will be moderated                             |
| DB_USER       | str  | True       | username of the database owner                                              |
| DB_PASS       | str  | True       | password from the database                                                  |
| DB_HOST       | str  | True       | IP address of the database                                                  |
| DB_NAME       | str  | True       | database name                                                               |
| PORT          | str  | True       | the database port. Usually the db running on port `5432`                    |
| SECRET_KEY    | str  | True       | secret key for django                                                       |
| API_KEY       | str  | True       | yandex api key for yandex map                                               |
| QIWI_KEY      | str  | True       | qiwi api key for receiving payments                                         |
| PHONE_NUMBER  | str  | True       | your phone number (need for qiwi)                                           |
| SECRET_P2     | str  | True       | public p2 key which allows you to issue an invoice and open a transfer form |
| USE_REDIS     | bool | False      | Optional parameter                                                          |

#### :green_book: Django

To create a `SECRET_KEY` you can use the site to [generate secret keys](https://djecrety.ir/)

And then paste it into the `.env` file

```dotenv
SECRET_KEY=jjv@^0qv^=aydunfjo$qpd_66j+)egm1#-c1iwt%mtjinm)ftj
```

Install the jazzmin

```sh
$ pip install -U django-jazzmin
```

To create required database tables and an admin user, use the following commands

```sh
$ python django_app.py makemigrations
$ python django_app.py migrate
$ python django_app.py createsuperuser
$ python django_app.py makemigrations usersmanage 
$ python django_app.py migrate usersmanage
$ python django_app.py runserver
```

## :see_no_evil: NudeNet

NudeNet is a collection of pre-classification and recognition models for nudity detection and censorship. This project
supports three different ways:

- Classification
- Detection
- Censoring images

In our case we use censoring images. For more information about this library, please
visit [the official repository at GitHub here](https://github.com/notAI-tech/NudeNet).

<b>Install TensorFlow</b>

If you have a GPU available, install the GPU based version of TensorFlow with the following command:

```sh
$ python -m pip install tensorflow-gpu==1.15
```

When using TensorFlow with support for GPU, be sure to have CUDA v10.0 installed on your system. Otherwise, use the CPU
based package:

```sh
$ python -m pip install tensorflow==1.15
```

<b>Install NudeNet</b>

You can install this module with the following command:

```sh
$ pip install --upgrade nudenet
```

The code that generates the censored image can be found on this path

```shell
$ DatingBot/utils/NudeNet/
```

And after that you need to run the file `app.py `

### :goal_net: Possible errors

```sh
$ ImportError: cannot import name '_registerMatType' from 'cv2.cv2' (...)
```

To solve this problem, you can install the previous version of opencv-python-headless

```sh
$ InvalidProtobuf: [ONNXRuntimeError] : 7 : INVALID_PROTOBUF : Load model from ./NudeNet/detector_v2_default_checkpoint.onnx failed:Protobuf parsing failed.
```

When running the first time, it will download the default checkpoint

Downloading the checkpoint to:

- <b>Windows</b> `C:/Users/username/.NudeNet/default/detector_v2_default_checkpoint.onnx`
- <b>MacOS</b>  `/Users/username/.NudeNet/detector_v2_default_checkpoint.onnx`
- <b>Linux</b> `/root/.NudeNet/detector_v2_default_checkpoint.onnx`

To solve this problem, first, you need to download checkpoint manually. You can find it
in [Releases](https://github.com/notAI-tech/NudeNet/releases/tag/v0)

After you have downloaded the checkpoint you need, drag it to the NudeNet folder

## :busts_in_silhouette: Contributing

### Code Style Guide

We try to stick
to [PEP 8](https://peps.python.org/pep-0008/#:~:text=Use%20the%20function%20naming%20rules,invoke%20Python's%20name%20mangling%20rules)

Thank you for your interest in contributing to our Python project! Below are the steps to help you become a part of our
developer community.

#### 1. Fork the Project

Go to the repository page on GitHub and click the "Fork" button in the upper right corner. This will create a copy of
the project in your account.

#### 2. Clone the Repository

```sh
$ git clone https://github.com/DavidRomanovizc/DatingBot.git
```

#### 3. Project Setup

For instructions on deploying the project on a local computer, see above

#### 4. Create a Branch

Create a new branch for your changes:

```sh
$ git checkout -b branch-name
```

#### 5. Make Changes

Make the necessary changes to the project code. Follow the project's structure, coding style, and development
guidelines.

And run the flake8

```sh
$ flake8 --config=.flake8
```

#### 6. Commit and Push

```sh
$ git commit -m "Description of your changes"
$ git push origin your-branch-name
```

#### 7. Create a Pull Request

Go to your repository on GitHub and click the "New Pull Request" button. Specify the base branch of the project (
usually `main` or `master`) and the branch with your changes.

#### 8. Discussion and Review

Discuss your Pull Request with the community members. Make necessary changes based on the feedback.

#### 9. Merge the Pull Request

After approval, your code will be merged into the main branch of the project.

#### 10. Celebration 🎉

Congratulations! You have successfully contributed to the Python project. Thank you for your help!

For multi languages we use i18n. All the instructions we can find here - [Language guide](lang_instruction.md)

<br><br/>

<h3 align="center">Works on Open Source</h3>

![image](https://user-images.githubusercontent.com/72649244/173241368-c40bd408-8df8-450f-9ac7-530de1692e1c.png)