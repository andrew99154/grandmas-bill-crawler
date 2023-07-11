from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

from billcrawlerforbot import *
import imageUploader

app = Flask(__name__)

channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get('CHANNEL_SECRET')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "帳單":
        target_file = get_pdf_file()
        store_path ="/tmp/"
        # imageUploader.upload_captcha()
        pdf_to_images(os.path.join(store_path,target_file),store_path)
        urls = imageUploader.upload_img()
        line_bot_api.reply_message(
            event.reply_token,
            [ImageSendMessage(original_content_url=urls[0],preview_image_url=urls[0]),
            ImageSendMessage(original_content_url=urls[1],preview_image_url=urls[1])])
        os.remove(os.path.join(store_path,target_file))
        # for f in os.listdir(store_path):
        #     print(f)
        print("send done!")
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="hihi!"))


if __name__ == "__main__":
    app.run()