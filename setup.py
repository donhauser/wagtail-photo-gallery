import setuptools

import os

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setuptools.setup(
    name='wagtail-photo-gallery',
    version='0.1.3',
    description='An image gallery plugin for Wagtail',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jonas Donhauser',
    #author_email='',
    url='https://github.com/donhauser/wagtail-photo-gallery',
    packages=['wagtail_photo_gallery'],
    package_data={
        '': ['LICENSE']
        + package_files('wagtail_photo_gallery/locale')
        + package_files('wagtail_photo_gallery/migrations')
        + package_files('wagtail_photo_gallery/static')
        + package_files('wagtail_photo_gallery/templates')
    },
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["wagtail>=4.1", "wagtail-generic-chooser>=0.2.1", "django-imagekit"],
    extras_require = {
        'pillow':["pillow"],
        'pillow-simd':["pillow-simd"],
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 4",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 4",
        "Framework :: Wagtail :: 5",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
