import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='wagtail-photo-gallery',
    version='0.0.2',
    description='An image gallery plugin for Wagtail',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jonas Donhauser',
    #author_email='',
    url='https://github.com/donhauser/wagtail-photo-gallery',
    packages=['wagtail_photo_gallery'],
    package_data={'': ['LICENSE', 'templates/*', 'static/*', 'migrations/*']},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["wagtail", "wagtail-generic-chooser", "django-imagekit"],
    extras_require = {
        'pillow':["pillow"],
        'pillow-simd':["pillow-simd"],
    },
)
