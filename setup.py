from setuptools import setup

setup(
    name='extract-email-from-http-header',
    version = "0.1.2",    
    description='Utility package to extract email from HTTP Request header.',
    url='https://github.com/NgZhengHan/extract-email-from-http-header',
    author='Ng Zheng Han',
    author_email='ng.zheng.han@gmail.com',
    packages=['extract_email_from_http_header'],    
    package_data={"": ["*"], },
    include_package_data=True,
    install_requires=['streamlit',                   
                      ],
)