label start:
    scene bg blck
    if not nama:
        $ nama = renpy.input("Masukkan nama kamu (max. 14 karakter)","cimo","abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ","{}",14)
    $ renpy.show_screen("history", _layer="master")
    python:
        ncolor = c.who_args["color"]
        prompt = renpy.input("{color=[ncolor]}[nama]{/color}")
        outval = dogpt(gptmodel,gpttemp,prompt)
        outval = outval[2:] if outval[:2] == "\n\n" else outval
        e.add_history(kind=nvl,who="GPT-Chan",what=outval)
        c.add_history(kind=nvl,who=nama,what=prompt)
    jump start