import urllib.request
import requests
import os
import glob
# from flask import Flask, redirect, render_template, request, session, url_for

def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def image_similar():
    if request.method == 'POST':
        url1 = request.args.get('url1', type = str)
        file_name1 = request.args.get('filename1', type = str)
        url = request.args.get('url2', type = str)
        file_name = request.args.get('filename2', type = str)

    download_image(url, 'uploads/', file_name)
    download_image(url1, 'uploads/', file_name1)

    import ResNet50_similarity as similarity
    d , t = similarity.similar()
    cwd_path = os.getcwd()
    data_path = cwd_path + '/uploads'
    filelist = glob.glob(os.path.join(data_path, "*"))
    for f in filelist:
        os.remove(f)
    message='ResNet50 image similarity_cosine: {:.2f}%'.format(t)
    print(message)
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
