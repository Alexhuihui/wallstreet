class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self,data):
        if data is None:
            return
        self.datas = data

    def output_html(self):
        fout = open('output.txt', 'w', encoding='utf-8')

        for data in self.datas:
            fout.write(data)

        fout.close()