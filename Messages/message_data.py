def isGif(message):
    if '.gif' in  message.lower():
        return True
    else:
        return False

def isMp4(message):
    if '.mp4' in  message.lower():
        return True
    else:
        return False

def isImage(message):
    image_formats = ['.png', '.jpeg', '.jpg', '.bmp']
    for image_type in  image_formats:
        if image_type in message.lower():
            return True
    return False

def isLink(message):
    if 'https' in message:
        return True
    return False


def parseMessage(message):
    split_text = message.split(" ")
    normal_text = ''
    data = {}
    other_info = {}
    for word in split_text:
        if isLink(word):
            if isImage(word):
                other_info = {
                    'type': 'image',
                    'link': word
                }
            elif isMp4(word):
                other_info = {
                    'type': 'video',
                    'link': word
                }
            elif isGif(word):
                other_info = {
                    'type': 'gif',
                    'link': word
                }
            else:
                other_info = {
                    'type': 'link',
                    'link': word
                }
        else:
            normal_text+=word+' '
    data = {
        'message': normal_text.rstrip(),
        'message_info': other_info
    }
    return data



def returnHTMLFormatted(messageJSON):
    for i in messageJSON:
        if i == 'message_info':
            if messageJSON[i]['type'] == 'image':
                img = '<img src"'+messageJSON[i]['link']+'">'
                print(img)
        print(messageJSON[i])
        print(i)

link = {'message': 'My name is mohamed Jama here is my image', 'message_info': {'link': 'https://i.imgur.com/ISt44aj.jpg', 'type': 'image'}}

print(returnHTMLFormatted(link))