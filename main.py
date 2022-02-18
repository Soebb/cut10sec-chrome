import os, datetime, glob, subprocess, json, time, asyncio
from telethon import TelegramClient, events, Button
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from persiantools import digits
import PTN
import keyboard as kb
import pygetwindow as gw
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BOT_TOKEN = " "
API_ID = " "
API_HASH = " "
BOT_NAME = "cuter-RoBot"

# system path to geckodriver.exe (Firefox driver)
driver_path = r""
Firefox_version = "97.0.1"

# namasha upload option
upload2namasha_option = True
url = "https://www.namasha.com/upload"
username = ""
password = ""


win = gw.getActiveWindow()

firefox_win = win #this will be a dynamic variable to store the Firefox window whenever be opened
if upload2namasha_option:
    os.environ['MOZ_FORCE_DISABLE_E105'] = Firefox_version


previous_cut_time = '02:00:04'

Bot = TelegramClient(BOT_NAME, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

refresh_button = [
    Button.inline(
        "Refresh List",
        data="refresh"
    )
]
msgid = 0
chatid = 0

def txtmsg(e,s,fa):
    ee = digits.to_word(int(e)) + "م"
    text = """
    `سریال {s} {fa} قسمت {e} با زیرنویس فارسی
    قسمت {ee} سریال {fa} {s} با زیرنویس چسبیده رایگان
    قسمت {e} سریال {fa} - {s} با زیرنویس فارسی چسبیده دی ال مکوین
    تماشای قسمت بعدی در کانال تلگرام ما :
    https://t.me/joinchat/Rguc8ahmI2pnKElU
    ,سریال {fa}
    ,{fa}
    ,{fa}{e}
    ,سریال {fa}{e}`
    ----------------------------------
    زیرنویس چسبیده قسمت {e} سریال ترکی {fa} قسمت {e} {s}
    قسمت {e} سریال {fa} با زیرنویس چسبیده قسمت {ee} {e} {s}
    سریال {fa} {e} {s} قسمت {ee} با زینویس چسبیده
    جهت دانلود تماشای کامل این قسمت کانال تلگرام دی ال مکوین شوید :
    https://t.me/joinchat/Rguc8ahmI2pnKElU
    ,سریال {fa}
    ,{fa}
    ,{fa}{e}
    ,سریال {fa}{e}
    """
    return text

@Bot.on(events.NewMessage(incoming=True, pattern="^/cancel"))
async def to_cancel(event):
    await event.reply('canceled.')
    exit(0)

@Bot.on(events.NewMessage(incoming=True, pattern="^/stop"))
async def to_stop(event):
    win.activate()
    kb.press_and_release('pause')
    await event.reply('stoped. to resume send /resume')

@Bot.on(events.NewMessage(incoming=True, pattern="^/resume"))
async def to_resume(event):
    win.activate()
    kb.press_and_release('enter')
    await event.reply('resumed.')


@Bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def start(event):
    keyboardd = []
    keyboardd.append(refresh_button)
    try:
        for file in glob.glob('C:/dlmacvin/1aa/*'):
            if file.endswith(('.ts', '.mp4', '.mkv')):
                keyboardd.append(
                    [
                        Button.inline(
                            file.rsplit('/', 1)[1].replace('1aa\\', ''),
                            data=file.rsplit('/', 1)[1].replace('1aa\\', '')
                        )
                    ]
                )
    except Exception as e:
        print(e)
        pass
    keyboardd.append(refresh_button)
    await event.reply("Which one?", buttons=keyboardd)


@Bot.on(events.CallbackQuery)
async def callback(event):
    global msgid, previous_cut_time, chatid, firefox_win
    if event.data == b"refresh":
        keyboardd = []
        keyboardd.append(refresh_button)
        try:
            for file in glob.glob('C:/dlmacvin/1aa/*'):
                if file.endswith(('.ts', '.mp4', '.mkv')):
                    keyboardd.append(
                        [
                            Button.inline(
                                file.rsplit('/', 1)[1].replace('1aa\\', ''),
                                data=file.rsplit('/', 1)[1].replace('1aa\\', '')
                            )
                        ]
                    )
        except Exception as e:
            print(e)
            return
        keyboardd.append(refresh_button)
        try:
            await event.edit(f"Which one of these {len(keyboard)} videos?", buttons=keyboardd)
        except:
            await Bot.send_message(event.chat_id, "error!! Send /start")
        return
    try:
        name = event.data.decode('utf-8')
        input = 'C:/dlmacvin/1aa/' + name
        metadata = extractMetadata(createParser(input))
        duration = int(metadata.get('duration').seconds)
        dtime = str(datetime.timedelta(seconds=duration))[:11]
        async with Bot.conversation(event.chat_id) as conv:
            ask = await conv.send_message(f'تایم کل ویدیو : {dtime} \n\nجهت کات ویدیو تایم را به این صورت ارسال کنید \n 00:00:00 02:10:00 \n\nOr send /previous to keep the previous cut time.')
            time = await conv.get_response()
            time2 = time.text

        if time2 == "/previous":
            end = previous_cut_time
        else:
            end = f'0{time2[:1]}:{time2[:3][1:]}:{time2[3:]}'
            previous_cut_time = end
        start = "00:00:00"
        await time.delete()
        await ask.delete()
        process_msg = await Bot.send_message(event.chat_id, "processing..\nFor cancel, send /cancel\nFor stop, send /stop")

        ext = '.' + name.rsplit('.', 1)[1]
        end_sec = sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(end.split(":"))))
        os.system(f'''ffmpeg -ss {start} -i "{input}" -to {end} -c copy -y "C:/dlmacvin/1aa/videos/{name.replace(ext, '-0'+ext)}"''')
        if upload2namasha_option:
            if firefox_win != win:
                try:
                    firefox_win.close()
                except:
                    pass
            driver=webdriver.Firefox(service=Service(driver_path), options=webdriver.FirefoxOptions())
            driver.get(url)
            firefox_win = gw.getActiveWindow()
            driver.find_element(By.ID, "UserName").send_keys(username)
            driver.find_element(By.ID, "Password").send_keys(password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

        cut_steps = []
        dif = duration - int(end_sec)
        for i in range(dif // 10):
            cut_steps.append(i * 10)
        for step in cut_steps:
            stp = str(end_sec + step)
            cut_name = name.replace(ext, '-'+str((step/10)+1)+ext)
            os.system(f'''ffmpeg -ss {start} -i "{input}" -to {stp} -c copy -y "C:/dlmacvin/1aa/videos/{cut_name}"''')
            if upload2namasha_option:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
                #await asyncio.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(url)
                firefox_win.activate()
                driver.find_element(By.XPATH, "//span[@class='btn btn-primary mt-4 px-3 py-2']").click()
                await asyncio.sleep(3)
                kb.write("C:\\dlmacvin\\1aa\\videos\\"+cut_name)
                kb.press_and_release('enter')
                await asyncio.sleep(3)
                driver.find_element(By.XPATH, '//input[@name="Title"]').send_keys(cut_name)

        await process_msg.delete()
        info=PTN.parse(name.replace(ext, ''))
        episode = str(info['episode'])
        episode = episode.split('0', 1)[1] if episode.startswith('0') else episode
        title = info['title']
        fa_name = serial_name(title)[1].replace(' #','').replace('# ','').replace('_',' ')
        latin_name = title.lower()
        if chatid == 0:
            msg = await Bot.send_message(event.chat_id, txtmsg(episode,latin_name,fa_name))
            msgid = msg.id
        elif chatid != 0:
            try:
                await Bot.edit_message(event.chat_id, msgid, txtmsg(episode,latin_name,fa_name))
            except:
                await Bot.edit_message(event.chat_id, msgid, 'تمام')
        chatid = event.chat_id
    except Exception as e:
        print(e)

def serial_name(m):
    fa = " "
    X = None
    if fa:
        if "Son Nefesime Kadar" in m:
            fa += "#تا_آخرین_نفسم"
        if "Maske Kimsin Sen" in m:
            fa += "#نقابدار_تو_کی_هستی؟"
        if "Etkileyici" in m:
            fa += "#تاثیرگذار"
        if "Emily in Paris" in m:
            fa += "#امیلی_در_پاریس"
        if "Gossip Girl" in m:
            fa += "#دختر_سخن_چین"
        if "The Great" in m:
            fa += "#کبیر"    
        if "The Witcher" in m:
            fa += "#ویچر"
        if "La Brea" in m:
            fa += "#لا_بریا"
        if "Annemizi Saklarken" in m:
            fa += "#وقتی_مادرمان_را_پنهان_میکردیم"
        if "Money Heist S05" in m:
            fa += "#خانه_کاغذی"
            X = "Money Heist S05" 
        if "Sakli" in m:
            fa += "#پنهان"
            X = "Sakli" 
        if "The Wheel of Time" in m:
            fa += "#چرخ_زمان"
            X = "The Wheel of Time"                      
        if "Foundation" in m:
            fa += "#بنیاد"
            X = "Foundation" 
        if "Hawkeye" in m:
            fa += "#هاکای"
            X = "Hawkeye" 
        if "The Lost Symbol" in m:
            fa += "#نماد_گمشده"
            X = "The Lost Symbol" 
        if "The Morning Show" in m:
            fa += "#نمایش_صبحگاهی"
            X = "The Morning Show" 
        if "The Umbrella Academy" in m:
            fa += "#آکادمی_آمبرلا"
            X = "The Umbrella Academy"
        if "Kulup" in m:
            fa += "#کلوپ"
            X = "Kulup"      
        if "Elbet Bir Gun" in m:
            fa += "#حتما_یه_روزی"
            X = "Elbet Bir Gun"
        if "Invasion" in m:
            fa += "#هجوم"
            X = "Invasion"
        if "Aziz" in m:
            fa += "#عزیز"
            X = "Aziz"
        if "Sana Soz" in m:
            fa += "#بهت_قول_میدم"
            X = "Sana Soz"
        if "Benim Hayatim" in m:
            fa += "#زندگی_من"
            X = "Benim Hayatim"
        if "Uc Kurus" in m:
            fa += "#سه_قرون"
            X = "Uc Kurus"
        if "Sen Cal Kapimi" in m:
            fa += "#تو_در_خانه_ام_را_بزن"
            X = "Sen Cal Kapimi"
        if "Dokhtarane Gol Foroosh" in m:
            fa += "#دختران_گل_فروش"
            X = "Dokhtarane Gol Foroosh"
        if "Marasli" in m:
            fa += "#اهل_ماراش"
            X = "Marasli"
        if "Kalp Yarasi" in m:
            fa += "#زخم_قلب"
            X = "Kalp Yarasi"
        if "Dunya Hali" in m:
            fa += "#احوال_دنیایی"
            X = "Dunya Hali"
        if "Ver Elini Ask" in m:
            fa += "#دستت_را_بده_عشق"
            X = "Ver Elini Ask"
        if "Ezel" in m:
            fa += "#ایزل"
            X = "Ezel"
        if "Ikimizin Sirri" in m:
            fa += "#راز_ما_دو_نفر"
            X = "Ikimizin Sirri"
        if "Dirilis Ertugrul" in m:
            fa += "#قیام_ارطغرل"
            X = "Dirilis Ertugrul"
        if "Yemin" in m:
            fa += "#قسم"
            X = "Yemin"
        if "Yargi" in m:
            fa += "#قضاوت"
            X = "Yargi"
        if "Ilk ve Son" in m:
            fa += "#اول_و_آخر"
            X = "Ilk ve Son"        
        if "See" in m:
            fa += "#دیدن"
            X = "See"        
        if "Ask i Memnu" in m:
            fa += "#عشق_ممنوع"
            X = "Ask i Memnu"
        if "Bozkir Arslani Celaleddin" in m:
            fa += "#جلال_الدین_خوارزمشاهی"
            X = "Bozkir Arslani Celaleddin"
        if "Kazara Ask" in m:
            fa += "#عشق_تصادفی"
            X = "Kazara Ask"
        if "Bas Belasi" in m:
            fa += "#بلای_جون"
            X = "Bas Belasi"
        if "Ask Mantik Intikam" in m:
            fa += "#عشق_منطق_انتقام"
            X = "Ask Mantik Intikam"
        if "Baht Oyunu" in m:
            fa += "#بازی_بخت"
            X = "Baht Oyunu"
        if "Ada Masali" in m:
            fa += "#قصه_جزیره"
            X = "Ada Masali"
        if "Askin Tarifi" in m:
            fa += "#طرز_تهیه_عشق"
            X = "Askin Tarifi"
        if "Yesilcam" in m:
            fa += "#سینمای_قدیم_ترکیه_فصل_دوم"
            X = "Yesilcam"
        if "Camdaki Kiz" in m:
            fa += "#دختر_پشت_پنجره"
            X = "Camdaki Kiz"
        if "Bir Zamanlar Kibris" in m:
            fa += "#روزی_روزگاری_در_قبرس"
            X = "Bir Zamanlar Kibris"
        if "Teskilat" in m:
            fa += "#تشکیلات"
            X = "Teskilat"
        if "Bizi Ayiran Oizgi" in m:
            fa += "#خط_فاصل_بین_ما"
            X = "Bizi Ayiran Oizgi"               
        if "Kardeslerim" in m:
            fa += "#خواهر_و_برادرانم"
            X = "Kardeslerim"
        if "Ogrenci Evi" in m:
            fa += "#خانه_دانشجویی"
            X = "Ogrenci Evi"
        if "Sihirli Annem" in m:
            fa += "#مادر_سحرآمیز_من"
            X = "Sihirli Annem"
        if "Yetis Zeynep" in m:
            fa += "#برس_زینب"
            X = "Yetis Zeynep"
        if "Hukumsuz" in m:
            fa += "#بی_قانون"
            X = "Hukumsuz"
        if "Saygi" in m:
            fa += "#احترام"
            X = "Saygi"
        if "Vahsi Seyler" in m:
            fa += "#چیز_های_وحشی"
            X = "Vahsi Seyler"
        if "Seref Bey" in m:
            fa += "#آقای_شرف"
            X = "Seref Bey"
        if "Gibi" in m:
            fa += "#مانند"
            X = "Gibi"
        if "Iste Bu Benim Masalim" in m:
            fa += "#این_داستان_من_است"
            X = "Iste Bu Benim Masalim"
        if "Akinci" in m:
            fa += "#مهاجم"
            X = "Akinci"
        if "Kirmizi Oda" in m:
            fa += "#اتاق_قرمز"
            X = "Kirmizi Oda"
        if "Emanet" in m:
            fa += "#امانت"
            X = "Emanet"
        if "Ibo Show" in m:
            fa += "#برنامه_ایبو_شو"
            X = "Ibo Show"
        if "EDHO" in m:
            fa += "#راهزنان"
            X = "EDHO"
        if "Uyanis Buyuk Selcuklu" in m:
            fa += "#بیداری_سلجوقیان_بزرگ"
            X = "Uyanis Buyuk Selcuklu"
        if "Yasak Elma" in m:
            fa += "#سیب_ممنوعه"
            X = "Yasak Elma"
        if "Sadakatsiz" in m:
            fa += "#بی_صداقت #بی_وفا"
            X = "Sadakatsiz"
        if "Bir Zamanlar Cukurova" in m:
            fa += "#روزی_روزگاری_چوکورا"
            X = "Bir Zamanlar Cukurova"
        if "Gonul Dagi" in m:
            fa += "#کوه_دل"
            X = "Gonul Dagi"
        if "Ufak Tefek Cinayetler" in m:
            fa += "#خرده_جنایت_ها"
            X = "Ufak Tefek Cinayetler"
        if "Sibe Mamnooe" in m:
            fa += "#سیب_ممنوعه"
            X = "Sibe Mamnooe"
        if "Setare Shomali" in m:
            fa += "#ستاره_شمالی"
            X = "Setare Shomali"
        if "Otaghe Ghermez" in m:
            fa += "#اتاق_قرمز"
            X = "Otaghe Ghermez"
        if "Mojeze Doctor" in m:
            fa += "#دکتر_معجزه_گر"
            X = "Mojeze Doctor"
        if "Mucize Doktor" in m:
            fa += "#دکتر_معجزه_گر"
            X = "Mucize Doktor"
        if "Be Eshghe To Sogand" in m:
            fa += "#به_عشق_تو_سوگند"
            X = "Be Eshghe To Sogand"
        if "Eshgh Az No" in m:
            fa += "#عشق_از_نو"
            X = "Eshgh Az No"
        if "Eshghe Mashroot" in m:
            fa += "#عشق_مشروط"
            X = "Eshghe Mashroot"
        if m.__contains__("Cukurova") and not m.__contains__("Bir"):
            fa += "#روزی_روزگاری_چکوروا"
            X = "Cukurova"
        if "Yek Jonun Yek Eshgh" in m:
            fa += "#یک_جنون_یک_عشق"
            X = "Yek Jonun Yek Eshgh"
        if "2020" in m:
            fa += "#2020"
            X = "2020"
        if "Hekim" in m:
            fa += "#حکیم_اوغلو"
            X = "Hekim"
        if "Godal" in m:
            fa += "#گودال"
            X = "Godal"
        if ("Cukur" in m) and not m.__contains__("Cukurova"):
            fa += "#گودال"
            X = "Cukur"
        if "Khaneh Man" in m:
            fa += "#سرنوشتت_خانه_توست"
            X = "Khaneh Man"
        if "Alireza" in m:
            fa += "#علیرضا"
            X = "Alireza"
        if "Dokhtare Safir" in m:
            fa += "#دختر_سفیر"
            X = "Dokhtare Safir"
        if "Marashli" in m:
            fa += "#ماراشلی - #اهل_ماراش"
            X = "Marashli"
        if "Zarabane Ghalb" in m:
            fa += "#ضربان_قلب"
            X = "Zarabane Ghalb"
        if "Aparteman Bigonahan" in m:
            fa += "#آپارتمان_بی_گناهان"
            X = "Aparteman Bigonahan" 
        if "Hayat Agaci" in m:
            fa += "#درخت_زندگی"
            X = "Hayat Agaci" 
        if "Ruya" in m:
            fa += "#رویا"
            X = "Ruya" 
        if "Uzak Sehrin Masali" in m:
            fa += "#داستان_شهری_دور"
            X = "Uzak Sehrin Masali"
        if "Icimizden Biri" in m:
            fa += "#یکی_از_میان_ما"
            X = "Icimizden Biri"
        if "Kocaman Ailem" in m:
            fa += "#خانواده_بزرگم"
            X = "Kocaman Ailem"
        if "Insanlik Sucu" in m:
            fa += "#جرم_انسانیت"
            X = "Insanlik Sucu"
        if "Tutsak" in m:
            fa += "#اسیر "
            X = "Tutsak"
        if "Fazilet Hanim ve Kızlari" in m:
            fa += "#فضیلت_خانم_و_دخترانش"
            X = "Fazilet Hanim ve Kızlari"
        if "Ferhat Ile Sirin" in m:
            fa += "#فرهاد_و_شیرین"
            X = "Ferhat Ile Sirin"
        if "Gel Dese Ask" in m:
            fa += "#عشق_صدا_میزند"
            X = "Gel Dese Ask"			
        if "Gibi" in m:
            fa += "#مانند"
            X = "Gibi"
        if "Halka" in m:
            fa += "#حلقه"
            X = "Halka"
        if "Hercai" in m:
            fa += "#هرجایی"
            X = "Hercai"
        if "Hizmetciler" in m:
            fa += "#خدمتکاران"
            X = "Hizmetciler"
        if "Istanbullu Gelin" in m:
            fa += "#عروس_استانبولی"
            X = "Istanbullu Gelin"
        if "Kalp Atisi" in m:
            fa += "#ضربان_قلب"
            X = "Kalp Atisi "
        if "Kara Sevda" in m:
            fa += "#کاراسودا #عشق_بی_پایان"
            X = "Kara Sevda"
        if "Kardes Cocuklari" in m:
            fa += "#خواهرزاده_ها"
            X = "Kardes Cocuklari"
        if "Kimse Bilmez" in m:
            fa += "#کسی_نمیداند"
            X = "Kimse Bilmez"
        if "Kursun" in m:
            fa += "#گلوله"
            X = "Kursun"
        if "Kuzey Yildizi Ilk Ask" in m:
            fa += "#ستاره_شمالی_عشق_اول"
            X = "Kuzey Yildizi Ilk Ask"
        if "Kuzgun" in m:
            fa += "#کلاغ #کوزگون"
            X = "Kuzgun"
        if "Meryem" in m:
            fa += "#مریم"
            X = "Meryem"
        if "Muhtesem Ikili" in m:
            fa += "#زوج_طلایی"
            X = "Muhtesem Ikili"
        if "Nefes Nefese" in m:
            fa += "#نفس_زنان"
            X = "Nefes Nefese"
        if "Ogretmen" in m:
            fa += "#معلم"
            X = "Ogretmen"
        if "Olene Kadar" in m:
            fa += "#تا_حد_مرگ"
            X = "Olene Kadar"
        if "Sahsiyet" in m:
            fa += "#شخصیت"
            X = "Sahsiyet"			
        if "Sahin Tepesi" in m:
            fa += "#تپه_شاهین"
            X = "Sahin Tepesi"
        if "Savasci" in m:
            fa += "#جنگجو"
            X = "Savasci"
        if "Sefirin Kizi" in m:
            fa += "#دختر_سفیر"
            X = "Sefirin Kizi"
        if "Sevgili Gecmis" in m:
            fa += "#گذشته_ی_عزیز"
            X = "Sevgili Gecmis"
        if "Sheref Bey" in m:
            fa += "#آقای_شرف"
            X = "Sheref Bey"
        if "Sihirlis Annem" in m:
            fa += "#مادر_جادویی_من"
            X = "Sihirlis Annem"
        if "The Protector" in m:
            fa += "#محافظ"
            X = "The Protector"
        if "Vahsi Seyler" in m:
            fa += "#چیزهای_وحشی"
            X = "Vahsi Seyler"
        if "Vurgun" in m:
            fa += "#زخمی"
            X = "Vurgun"
        if "Ya Istiklal Ya Olum" in m:
            fa += "#یا_استقلال_یا_مرگ"
            X = "Ya Istiklal Ya Olum"
        if ("Yalanci" in m) and not m.__contains__("Yalancilar ve Mumlari"):
            fa += "#دروغگو"
            X = "Yalanci"
        if "El Kizi" in m:
            fa += "#دختر_مردم"
            X = "El Kizi"
        if "Masumlar Apartmani" in m:
            fa += "#آپارتمان_بیگناهان"
            X = "Masumlar Apartmani"
        if "Yalancilar ve Mumlari" in m:
            fa += "#دروغگو_ها_و_شمع_هایشان"
            X = "Yalancilar ve Mumlari"
        if "Lise Devriyesi" in m:
            fa += "#گشت_مدرسه"
            X = "Lise Devriyesi"
        if "Evlilik Hakkinda Her Sey" in m:
            fa += "#همه_چیز_درباره_ازدواج"
            X = "Evlilik Hakkinda Her Sey"
        if "Son Yaz" in m:
            fa += "#آخرین_تابستان"
            X = "Son Yaz"
        if "Barbaroslar Akdenizin Kilici" in m:
            fa += "#بارباروس_ها_شمشیر_دریای_مدیترانه"
            X = "Barbaroslar Akdenizin Kilici"
        if "Bir Ask Hikayesi" in m:
            fa += "#حکایت_یک_عشق"
            X = "Bir Ask Hikayesi"
        if "Carpisma" in m:
            fa += "#تصادف"
            X = "Carpisma"
        if "Cocuk" in m:
            fa += "#بچه"
            X = "Cocuk"
        if "Lise Devriyesi" in m:
            fa += "#گشت_مدرسه"
            X = "Lise Devriyesi"
        if "Kurulus Osman" in m:
            fa += "#قیام_عثمان"
            X = "Kurulus Osman"
        if "Kanunsuz Topraklar" in m:
            fa += "#سرزمین_های_بی_قانون"
            X = "Kanunsuz Topraklar"
        if "Kibris Zafere Dogru" in m:
            fa += "#قبرس_پیش_به_سوی_پیروزی"
            X = "Kibris Zafere Dogru"
        if "Misafir" in m:
            fa += "#مهمان"
            X = "Misafir"
        if "Eskiya Dunyaya Hukumdar Olmaz" in m:
            fa += "#راهزنان "
            X = "EDHO"
        if "Kaderimin Oyunu" in m:
            fa += "#بازی_تقدیرم"
            X = "Kaderimin Oyunu"
        if "Squid Game" in m:
            fa += "#بازی_مرکب"
            X = "Squid Game"
        if "Alparslan Buyuk Selcuklu" in m:
            fa += "#آلپ_ارسلان_سلجوقیان_بزرگ"
            X = "Alparslan Buyuk Selcuklu"
        if "Elkizi" in m:
            fa += "#دختر_مردم"
            X = "Elkizi"
        if "Masumiat" in m:
            fa += "#معصومیت"
            X = "Masumiat"
        if "Destan" in m:
            fa += "#حماسه"
            X = "Destan"
        if "Hamlet" in m:
            fa += "#هملت"
            X = "Hamlet"
        if "Mahkum" in m:
            fa += "#محکوم"
        if "Chapelwaite" in m:
            fa += "#چپلویت"
        if "El Cid" in m:
            fa += "#ال _ید"
        if "Grimm" in m:
            fa += "#گریم"
        if "Heels" in m:
            fa += "#هیلز"
        if "Maid" in m:
            fa += "#خدمتکار "
        if "Mayor of Kingstown" in m:
            fa += "#شهردار_کینگزتاون"
        if "Only Murders in the Building" in m:
            fa += "#فقط_قتل_های_این_ساختمان"
        if "Scenes from a Marriage" in m:
            fa += "#صحنه_هایی_از_یک_ازدواج"            
        if "Skam" in m:
            fa += "#شرم"
        if "The Chestnut Man" in m:
            fa += "#مرد_بلوطی"
        if "Titans" in m:
            fa += "#تایتان ها"            
        if "War And Peace" in m:
            fa += "#جنگ_و_صلح"
        if "Yellowjackets" in m:
            fa += "#ژاک_ زرد"
        if "You" in m:
            fa += "#تو"
        if "Erkek Severse" in m:
            fa += "#اگر_مرد_دوست_داشته_باشد"
    return X, fa


Bot.run_until_disconnected()
