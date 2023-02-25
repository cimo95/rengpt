define config.name = _("RenGPT")
define gui.show_name = True
define config.version = "1.0"
define gui.about = _p("""
""")
define build.name = "RenGPT"
define config.has_sound = True
define config.has_music = True
define config.has_voice = True
define gui.history_height = None

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None
define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)
define config.developer = False
define config.history_length = 5000
define config.thumbnail_width = 256
define config.thumbnail_height = 144

default preferences.text_cps = 0
default preferences.afm_time = 15

define config.save_directory = "RenGPT-1677056362"
define config.window_icon = "gui/window_icon.png"

define e = Character('GPT-chan', color="#c8ffc8")
define c = DynamicCharacter('nama', color="#64cff0")
define gptmodel = "text-davinci-003"
define gpttemp = 0.9
define nama = ""
define persistent.savemode = 0


image bg blck = Solid("#000000")

init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**.rpy', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.documentation('*.html')
    build.documentation('*.txt')

    def dogpt(model,iTemp,prompt):
        import requests
        sKey = open(config.basedir.replace('\\','/')+"/game/apikey.txt","r").read()
        sModel = "text-davinci-003"

        URL = 'https://api.openai.com/v1/completions'

        HEADER = {
            'Accept':'application/json',
            'Content-Type':'application/json',
            'Authorization':'Bearer '+sKey
        }

        PARAM = {
            'model' : sModel,
            'prompt' : prompt,
            'temperature' : iTemp,
            'max_tokens' : 150,
            'top_p' : 1,
            'frequency_penalty' : 0.0,
            'presence_penalty' : 0.6,
            'stop' : '[" Human:", " AI:"]'
        }

        req = requests.post(url=URL, headers=HEADER, json=PARAM)
        jData =req.json()
        try:
            sOut = jData['choices'][0]['text']
            sOut = sOut[:sOut.rfind('.')+1]
        except:
            sOut = "\bGagal mengakses server ChatGPT.\nPastikan internet anda stabil, dan anda sudah menyimpan API KEY anda\ndi file \"apikey.txt\" dalam folder \"game\""
        return sOut

    def docopy(text):
        import pygame.scrap
        try:
            pygame.scrap.init()
            pygame.scrap.put(pygame.SCRAP_TEXT, bytes(text, 'utf-8'))
            renpy.notify("Teks berhasil disalin ke papan klip.")
        except:
            renpy.notify("Teks gagal disalin ke papan klip.")

    def doekspor():
        from datetime import datetime
        dtSkrg = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        sExp = ".csv" if persistent.savemode == 0 else ".txt"
        fData = open(config.basedir.replace("\\","/")+"/renGPT-"+dtSkrg+sExp,"w")
        iCd = 0
        lTemp = []
        sLine = ""
        if persistent.savemode == 0:
            fData.write("sep=,\n")
            for hItem in list(reversed(_history_list)):
                iCd += 1
                sLine += '"'+hItem.who+'","'+hItem.what+'"\n'
                if iCd >= 2:
                    lTemp.append(sLine+'"",""\n')
                    iCd = 0
                    sLine = ""
            for lItem in list(reversed(lTemp)):
                fData.write(lItem)
            fData.close()
        else:
            for hItem in list(reversed(_history_list)):
                iCd += 1
                sLine += ''+hItem.who+':\n"'+hItem.what+'"\n'
                if iCd >= 2:
                    lTemp.append(sLine+'\n')
                    iCd = 0
                    sLine = ""
            for lItem in list(reversed(lTemp)):
                fData.write(lItem)
            fData.close()            
        renpy.notify("Riwayat prompt RenGPT berhasil disimpan sebagai renGPT-"+dtSkrg+sExp+".")

