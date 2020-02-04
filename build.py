#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys


def calc_page_str(_p):
    if _p == 1:
        return ''
    else:
        return _p


def make_pager(total, cur):
    page_html = '<div class="w3-center w3-padding-32"><div class="w3-bar">'
    if cur > 1:
        page_html += '<a href="index{0}.html" class="w3-bar-item w3-button w3-hover-black">«</a>'.format(
            calc_page_str(cur - 1))
    for i in range(total):
        if i + 1 == cur:
            page_html += '<a href="index{0}.html" class="w3-bar-item w3-button w3-black">{1}</a>'.format(
                calc_page_str(i + 1), i + 1)
        else:
            page_html += '<a href="index{0}.html" class="w3-bar-item w3-button w3-hover-black">{1}</a>'.format(
                calc_page_str(i + 1), i + 1)
    if cur < total:
        page_html += '<a href="index{0}.html" class="w3-bar-item w3-button w3-hover-black">»</a>'.format(
            calc_page_str(cur + 1))
    page_html += '</div></div>'
    return page_html


def make_html_before(_title, _subtitle):
    return '''
<html lang="zh">
<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>''' + _title + '''</title><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="./css/w3.css">
<style>
body, h1 {font-family: "Montserrat", sans-serif;}
.img {margin-bottom: -7px;width: 100%;min-height:300px;}
.w3-row-padding img {margin-bottom: 12px;}
</style>
</head>
<body>
<div class="w3-content" style="max-width:1500px">
<div class="w3-opacity"><header class="w3-center w3-margin-bottom"><h1><b>''' + _title + '''</b></h1><p><b>''' + _subtitle + '''</b></p></header></div>
<div class="w3-row-padding">
'''


def make_html_end(_title):
    return '''
</div>
<footer class="w3-container w3-padding-64 w3-light-grey w3-center w3-opacity w3-xlarge" style="margin-top:128px"><p class="w3-medium">&copy; 
''' + _title + '''
</p></footer>
<script>
    function getOffsetByBody(el) {
        let offsetTop = 0;
        while (el && el.tagName !== 'BODY') {
            offsetTop += el.offsetTop;
            el = el.offsetParent;
        }
        return offsetTop;
    }

    function lazyLoad() {
        let img = document.getElementsByClassName('img');
        let availHeight = window.screen.availHeight;
        let scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
        for (let i = 0; i < img.length; i++) {
            let offsetTop = getOffsetByBody(img[i]);
            console.log(offsetTop);
            if (offsetTop - scrollTop < availHeight) {
                let src = img[i].getAttribute('data-src');
                if (src) {
                    img[i].setAttribute('src', src);
                    img[i].removeAttribute('data-src');
                }
            }
        }
    }
    window.onload = lazyLoad;
    window.onscroll = lazyLoad;
</script>
</body>
</html>
'''


def listdir_no_hidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


if __name__ == '__main__':
    title = ''
    subtitle = ''
    if len(sys.argv) > 1:
        title = sys.argv[1]
    else:
        title = input('Input title:')
    if len(sys.argv) > 2:
        subtitle = sys.argv[2]
    else:
        subtitle = input('Input subtitle:')
    print('Generate successful.')
    img_list = [elem for elem in os.listdir('img') if not elem.startswith('.')]
    total_num = int(len(img_list) / 18) + 1

    content = ['<div class="w3-third">', '<div class="w3-third">', '<div class="w3-third">']

    i = 0
    for img in img_list:
        content[i % 3] += '<img class="img" data-src="./img/' + img + '" alt="">'
        i += 1
        if i % 18 == 17 or i == len(img_list) - 1:
            p = int(int(i / 18) + 1)
            filename = 'index{0}.html'.format(p)
            if p == 1:
                filename = 'index.html'
            html = make_html_before(title, subtitle) \
                   + content[0] + '</div>' \
                   + content[1] + '</div>' \
                   + content[2] + '</div></div>' \
                   + make_pager(total_num, p) + make_html_end(title)
            with open(filename, 'w', encoding='utf-8') as file_object:
                file_object.write(html)
                file_object.close()
            content = ['<div class="w3-third">', '<div class="w3-third">', '<div class="w3-third">']
