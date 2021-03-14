import eel, desktop, time
from datetime import datetime as dt
import spreadsheetManager, dataManager, fileManager
import mercari

app_name="html"
end_point="index.html"
size=(800,600)

@ eel.expose
def load_spreadsheet_list():
    file = 'spreadsheet_list.csv'
    spreadsheets = fileManager.read_csv_file(file)
    option_list = []
    for spreadsheet in spreadsheets:
        eel.add_option(spreadsheet[0])

@ eel.expose
def start(url: str):
    print("start button pressed")
    # 変数設定
    spreadsheet_list = fileManager.read_csv_file("spreadsheet_list.csv")
    URL = spreadsheet_list[spreadsheet_number][0]
    JSONKEY = spreadsheet_list[spreadsheet_number][1]

    # google spreadsheetに接続・データ抽出
    sheet = spreadsheetManager.connect_to(JSONKEY, URL, 0)
    sheet_data = spreadsheetManager.fetch_allData(sheet)

    # headerとdataを分離する
    header = sheet_data[0]
    data = sheet_data[1:]

    # ログインは不要
    mercari.start()
    
    # 抽出データの処理
    for row, datum in enumerate(data):
        print('datum:', datum)
        mercari.go_to_sell_page()

        item_info = dataManager.get_dummy_item_info() # get_item_info(datum)
        delivery_info = dataManager.get_dummy_shippment_info() # get_delivery_info(datum)

        ## 出品時間を決めたいならここにタイマー

        ## 処理的なもの 出品 / 値下げ / 取下げ の条件分岐をここで datumにitemの状態(mercari_status)を表す値必要
        mercari.sell_item(item_info, delivery_info)
        mercari.send_input()

        if row != len(data) - 1:
            print("続けて出品するよ")
            mercari.continue_sell()

        ## timer的なものがあるなら、ここに記述し、タイミングを図る

        if row == 1:
            break

    # ブラウザを閉じて終了
    # mercari.close()


desktop.start(app_name,end_point,size)
