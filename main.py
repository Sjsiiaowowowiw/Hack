#Không hiểu về code xem kĩ video
import telebot
import datetime
import time
import os
import re
import subprocess
import requests
import sys
#Điền bot token của bạn
bot_token = '6748031892:AAFYLvQPnPcL3cOfh-BCzMcfDQF25Bzz1QE'
bot = telebot.TeleBot(bot_token)
#Điền id tele của mình
processes = []
ADMIN_ID = '5968619607'

def TimeStamp():
    return str(datetime.date.today())

def get_user_file_path(user_id):
    today_day = datetime.date.today().day
    user_dir = f'./user/{today_day}'
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return f'{user_dir}/{user_id}_key.txt'

def is_key_expired(user_id):
    file_path = get_user_file_path(user_id)
    if not os.path.exists(file_path):
        return True
    with open(file_path, 'r') as f:
        timestamp = f.read().strip()
    try:
        key_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
    except ValueError:
        return True
    return (datetime.datetime.now() - key_time).days >= 1

@bot.message_handler(commands=['getkey'])
def startkey(message):
    bot.reply_to(message, text='Vui Lòng Chờ😪')
    user_id = message.from_user.id
    if is_key_expired(user_id):
        key = "thanhdev" + str(int(user_id) * int(datetime.date.today().day) - 12666)
        key = "https://bio.link/thanhdevtool/?key=" + key
        api_token = ''
        url = requests.get(f'https://link4m.co/api-shorten/v2?api=662270a8632b4b42511ca862&url={api_token}&url={key}').json()
        url_key = url['shortenedUrl']
        with open(get_user_file_path(user_id), 'w') as f:
            f.write(TimeStamp())
        text = f'''
- LINK LẤY KEY {TimeStamp()} LÀ: {url_key} -
- KHI LẤY KEY XONG, DÙNG LỆNH /key <key> ĐỂ TIẾP TỤC -
        '''
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, 'Bạn Đã GetKey Rồi💤')

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Vui Lòng Nhập Key🔑')
        return

    user_id = message.from_user.id
    key = message.text.split()[1]
    expected_key = "thanhdev" + str(int(user_id) * int(datetime.date.today().day) - 12666)
    
    if key == expected_key:
        bot.reply_to(message, 'Key Hợp Lệ Bạn Được Phép Dùng Lệnh /spam.')
        with open(get_user_file_path(user_id), "w") as f:
            f.write(TimeStamp())
    else:
        bot.reply_to(message, 'Key Sai Vui Lòng Kiểm Tra Lại Hoặc Lh Admin')

@bot.message_handler(commands=['superspam'])
def superspam(message):
    user_id = message.from_user.id
    if not os.path.exists(f"./vip/{user_id}.txt"):
        bot.reply_to(message, 'Đăng Kí Vip Đi Rẻ Lắm😭')
        return
    with open(f"./vip/{user_id}.txt") as fo:
        data = fo.read().split("|")
    past_date = data[0].split('-')
    past_date = datetime.date(int(past_date[0]), int(past_date[1]), int(past_date[2]))
    today_date = datetime.date.today()
    days_passed = (today_date - past_date).days
    if days_passed < 0:
        bot.reply_to(message, 'Key Vip Cài Vào ngày khác')
        return
    if days_passed >= int(data[1]):
        bot.reply_to(message, 'Key Vip Hết Hạn Mua Típ Đi😪')
        os.remove(f"./vip/{user_id}.txt")
        return
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI')
        return
    if len(message.text.split()) == 2:
        bot.reply_to(message, 'Thêm số lần đ m!!!')
        return
    lap = message.text.split()[2]
    if lap.isnumeric():
        if not (1 <= int(lap) <= 30):
            bot.reply_to(message, "Spam Không Hợp Lệ Chỉ Spam Từ 1-30 Lần🚨")
            return
    lap = message.text.split()[2]
    if not lap.isnumeric():
        bot.reply_to(message, "Sai dữ kiện !!!")
        return
    phone_number = message.text.split()[1]
    if not re.search(r"^(?:\+84|0)(3[2-9]|5[6-9]|7[0-9]|8[0-689]|9[0-4])[0-9]{7}$", phone_number):
        bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
        return
    if phone_number in ["0528300000"]:
        bot.reply_to(message, "Spam cái đầu buồi tao huhu")
        return
    file_path = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, lap])
    processes.append(process)
    bot.reply_to(message, f'🌠 Tấn Công Thành Công 🌠 \n+ Bot 👾: @quydepzai_bot \n+ Số Tấn Công 📱: [ {phone_number} ]\n+ Lặp lại : {lap}\n+ Admin 👑: @thanngheo2002\n+ Tiktok : Quý Quý\n+ Key : vip')

@bot.message_handler(commands=['spam'])
def spam(message):
    user_id = message.from_user.id
    if not os.path.exists(get_user_file_path(user_id)):
        bot.reply_to(message, 'Dùng /getkey để lấy key và dùng /key để nhập key hôm nay')
        return
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI')
        return
    if len(message.text.split()) == 2:
        bot.reply_to(message, 'Thiếu dữ kiện !!!')
        return
    lap = message.text.split()[2]
    if lap.isnumeric():
        if not (1 <= int(lap) <= 10):
            bot.reply_to(message, "Spam Không Hợp Lệ Chỉ Spam Từ 1-10 Lần🚨")
            return
    else:
        bot.reply_to(message, "Sai dữ kiện !!!")
        return
    phone_number = message.text.split()[1]
    if not re.search(r"^(?:\+84|0)(3[2-9]|5[6-9]|7[0-9]|8[0-689]|9[0-4])[0-9]{7}$", phone_number):
        bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
        return
    if phone_number in ["0528300000"]:
        bot.reply_to(message, "Spam cái đầu buồi tao huhu")
        return
    file_path = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, lap])
    processes.append(process)
    bot.reply_to(message, f'🌠 Tấn Công Thành Công 🌠 \n+ Bot 👾: @quydepzai_bot \n+ Số Tấn Công 📱: [ {phone_number} ]\n+ Lặp lại : {lap}\n+ Admin 👑: @thanngheo2002\n+ Tiktok : QuýQuý\n+ Key : free')

@bot.message_handler(commands=['help'])
def help(message):
    help_text = '''
Danh sách lệnh:
┌───────────────⭓ 
│• /getkey: Lấy Key Dùng Lệnh🔑
│• /key {key}: Nhập key Thường🔒
│• /spam : Spam free📱
│• /superspam : SpamVip🎗️
│• /help: Danh sách lệnh📄
│• /thongtin : Share Intro🌸Tool
│• /status : Admin
│• /restart : Admin
│• /stop : Admin
│• /them : Admin
└────────────────
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Làm Cái Trò Gì Zậy😀')
        return
    process_count = len(processes)
    bot.reply_to(message, f'Số quy trình đang chạy: {process_count}.')

@bot.message_handler(commands=['restart'])
def restart(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Làm Cái Trò Gì Zậy😀')
        return
    bot.reply_to(message, 'Bot sẽ được khởi động lại trong giây lát...')
    time.sleep(2)
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Làm Cái Trò Gì Zậy😀')
        return
    bot.reply_to(message, 'Bot sẽ dừng lại trong giây lát...')
    time.sleep(2)
    bot.stop_polling()

@bot.message_handler(commands=['them'])
def them(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Làm Cái Trò Gì Zậy😀')
        return
    try:
        idvip = message.text.split()[1]
        ngay = message.text.split()[2]
        hethan = message.text.split()[3]
        with open(f"./vip/{idvip}.txt", "w") as fii:
            fii.write(f"{ngay}|{hethan}")
        bot.reply_to(message, f'Thêm Thành Công {idvip} Làm Vip')
    except IndexError:
        bot.reply_to(message, 'Vui lòng cung cấp đủ thông tin: /them <idvip> <ngay> <hethan>')

@bot.message_handler(commands=['thongtin'])
def thongtin(message):
    reply_text = 'All Tool Của Admin👇:\n\n'
    reply_text += '- DIE R\n'
    reply_text += '- FB: QUYGIA\n'
    reply_text += '- Tiktok: ............\n'
    reply_text += '- KeyVip Vĩnh Viễn 150k\n'
    reply_text += '- KeyVip 30 ngày 50k \n'
    bot.reply_to(message, reply_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Lệnh Không Hợp lệ Vui Lòng Ghi /help để xem các lệnh📄')

bot.polling()