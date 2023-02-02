from flask import Flask, request, send_file
import zipfile
import os

class ZipFileUploader:
    def __init__(self,name):
        self.app=Flask(name)

    def html_code(self):
        return '''
            <form action="/" method="post" enctype="multipart/form-data">
                <input type="file" name="zip_files" multiple>
                <input type="submit" value="Upload">
            </form>        '''

    def upload_zip_files(self):
        if request.method == 'POST':
            zip_files = request.files.getlist('zip_files')
            if zip_files:
                return self.extract_zip_files(zip_files)
        return self.html_code()

    def extract_zip_files(self, zip_files):
        extracted_files = []
        for zip_file in zip_files:
            try:
                with zipfile.ZipFile(zip_file, 'r') as z:
                    z.extractall()
                    extracted_files += z.namelist()
            except Exception as e:
                return 'Error in extracting files: ' + str(e)
        return '<br>'.join(extracted_files) + '<br><br>Files Extracted Successfully!'

    def download_file(self, filename):
        try:
            return send_file(os.path.join('extracted_files', filename), as_attachment=True)
        except Exception as e:
            return 'Error in downloading file: ' + str(e)

    def run(self):
        self.app.add_url_rule('/', 'upload_zip_files', self.upload_zip_files, methods=['GET', 'POST'])
        self.app.add_url_rule('/download/<filename>', 'download_file', self.download_file)
        self.app.run()


if __name__ == '__main__':
    ZipFileUploader('ZipFileUploader').run()

