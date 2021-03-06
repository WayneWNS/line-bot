# 架設網站最有名的兩種 flask, django
# 這是一個web app = 放在網路上執行的程式；練習時在CMD上執行的程式是local app

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('k/JtCrIqadRd47SHYTW7INrc+K7OM6Y5Ze8Qgs54/DkTfXKCaflTqGZOAX74FXiIwPZzvHPrVFsrQPUKRYlSY3jUI+PnTOgaQuDmzKjV/3cgBGVqFhE+ma8R2acnh05W3rJgkakHD5kQza63sU31NwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ecc4572344a78b22dfd12f82b99e0279')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '哩供蝦!'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return

    if msg in ['hi', 'Hi']:
        r = '嗨!'
    elif msg == '吃飯沒':
        r = '還沒，你要請嗎?'
    elif '午餐' in msg:
        r = '吃自己吧'
    elif '嗆' in msg:
        r = '剛好而已啦'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()