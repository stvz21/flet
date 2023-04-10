from flett import Flett, request
from tqdm import tqdm
import requests
import json

app = Flett(__name__)

@app.route('/download', methods=['POST'])
def download_files():
    session = requests.Session()
    login_data = {
        'username': "stvz02",
        'password': "stvz02**"
    }
    session.post("https://anuarioeco.uo.edu.cu/index.php/aeco/login/signIn", data=login_data)
    input_str = request.form['input_str']
    try:
        files_dict = json.loads(input_str)
        if isinstance(files_dict, dict):
            files_dict = [files_dict]
    except:
        id_archive, filename = input_str.split()
        files_dict = [{"id": id_archive, "name": filename}]
    for file_dict in files_dict:
        id_archive = file_dict["id"]
        filename = file_dict["name"]
        download_url = f'https://anuarioeco.uo.edu.cu/index.php/aeco/$$$call$$$/api/file/file-api/download-file?submissionFileId={id_archive}&submissionId=5736&stageId=1'
        response = session.head(download_url)
        response = session.get(download_url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open('/storage/emulated/0/Download/'+filename, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()
    return 'Archivos descargados con éxito!'

if __name__ == '__main__':
    app.run()
