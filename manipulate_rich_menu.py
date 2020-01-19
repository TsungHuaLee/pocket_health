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
                action=PostbackAction(label='postback', data='richmenu_chronic')),
            RichMenuArea(
                bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
                action=PostbackAction(label='postback', data='richmenu_goodbody')),
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=843, width=1250, height=843),
                action=PostbackAction(label='postback', data='richmenu_health')),
            RichMenuArea(
                bounds=RichMenuBounds(x=1250, y=843, width=1250, height=843),
                action=PostbackAction(label='postback', data='richmenu_supply'))
                ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    print(rich_menu_id)
    with open("rich-menu-id.txt", "a+") as fp:
        fp.write(rich_menu_id)

def upload_png_to_richmenu(rich_menu_id):
    file_path = "linebot-rich-menu_2500x1686.png"
    content_type = "image/png"
    with open(file_path, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)
    
def set_default_rich_menu(rich_menu_id):
    line_bot_api.set_default_rich_menu(rich_menu_id)

if __name__ == "__main__":
    # upload_png_to_richmenu("richmenu-4f2e64918ea925fafab80df6c49f1814")
    # set_default_rich_menu("richmenu-4f2e64918ea925fafab80df6c49f1814")