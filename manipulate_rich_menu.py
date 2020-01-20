from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.models import PostbackAction, MessageAction
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds
from pocket_health.settings import LINE_ACCESS_TOKEN

Line_Access_Token = LINE_ACCESS_TOKEN

line_bot_api = LineBotApi(Line_Access_Token)

def create_rich_menu():
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=False,
        name="pocket_health",
        chat_bar_text="服務選單",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
                action=PostbackAction(label='postback', data='richmenu_chronic', display_text='我想更瞭解慢性病')),
            RichMenuArea(
                bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
                action=PostbackAction(label='postback', data='richmenu_assessment', display_text='身體狀況評估')),
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=843, width=1250, height=843),
                action=PostbackAction(label='postback', data='richmenu_counseling', display_text='健康諮詢')),
            RichMenuArea(
                bounds=RichMenuBounds(x=1250, y=843, width=1250, height=843),
                action=PostbackAction(label='postback', data='richmenu_supply', display_text='為您推薦'))
                ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    print(rich_menu_id)
    with open("rich-menu-id.txt", "a+") as fp:
        fp.write(rich_menu_id)

    return rich_menu_id

def upload_png_to_richmenu(rich_menu_id):
    file_path = "linebot-rich-menu_2500x1686_v2.png"
    content_type = "image/png"
    with open(file_path, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)
    return True
    
def set_default_rich_menu(rich_menu_id):
    line_bot_api.set_default_rich_menu(rich_menu_id)

if __name__ == "__main__":
    rich_menu_id = create_rich_menu()
    status = upload_png_to_richmenu(rich_menu_id)
    if(status==True):
        set_default_rich_menu(rich_menu_id)
    print("Successfully")