from html.parser import HTMLParser
from html.entities import name2codepoint
import json
from json import JSONEncoder

class Verse:
    versNumber = ""
    lines = ""

    def __init__(self, versNumber):
        self.versNumber = versNumber

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global prevTag
        prevTag = tag
        global prevAttr
        if not 'br' in tag:
            #print("Start tag:", tag)
            for attr in attrs:
                #print("     attr:", attr)
                prevAttr = attr

    #def handle_endtag(self, tag):
     #   if 'prevTag' in globals():
      #      if ('dd' in prevTag or 'span' in prevTag or 'dl' in prevTag or 'dt' in prevTag or 'br' in prevTag)\
       #             and 'br' not in tag:
        #        print("End tag  :", tag)

    def handle_data(self, data):

        if 'prevAttr' in globals() and data.strip() != '':
            #if ('songinfo' in prevAttr or 'versenumber' in prevAttr or 'songtitle' in prevAttr or 'versebody' in prevAttr or 'bibleverse' or 'chorus' in prevAttr or 'songnumberlink pcalibre pcalibre1 pcalibre2' in prevAttr)\
            #and not data.isspace() and "[Index]" not in data:
                #print(data.strip())

            if 'songnumberlink pcalibre pcalibre2 pcalibre1' in prevAttr and "[Index]" not in data and not data.isspace() and 'song' in globals():
                song["songNumber"] = data.strip()

            if 'songinfo' in prevAttr and not data.isspace() and 'song' in globals():
                song["songInfo"] += data.strip() + "\n"

            if 'songtitle' in prevAttr and not data.isspace() and 'song' in globals():
                song["songTitle"] = data.strip()

            if 'versenumber' in prevAttr and not data.isspace() and 'song' in globals():
                song["verses"].append({"versNumber": data, "lines": ''})

            if 'versebody' in prevAttr or 'chorus' in prevAttr and not data.isspace() and 'song' in globals():
                currentVers = song["verses"][-1]
                if currentVers.get("lines") == '':
                    currentVers['lines'] += data.strip()
                else:
                    currentVers['lines'] += '\n' + data.strip()

            if 'bibleverse' in prevAttr and not data.isspace() and 'song' in globals():
                song["footer"] = data.strip()


    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)

if __name__ == '__main__':
    parser = MyHTMLParser()
    songs = []
    i = 1
    while i <= 472:
        global song
        song = {
            "songNumber": "",
            "songInfo": "",
            "verses": []
        }
        parser.feed(open("input/songs_split_" + str(i).zfill(3) + ".html", encoding='utf-8').read())
        songs.append(song)
        i += 1
    data = json.dumps(songs, indent=2)
    f = open("output.json", "a")
    f.write(data)
    f.close()
    print('done')

