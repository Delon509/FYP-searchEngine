import mysql.connector
import json
from decouple import config



class Document:
    def __init__(self,index,title,url,content,description,containImage,listImageDescription,containVideo,listVideoDescription):
        self.index=index
        self.title=title
        self.url=url
        self.content=content
        self.description=description
        self.containImage=containImage
        self.listImageDescription=listImageDescription
        self.containVideo=containVideo
        self.listVideoDescription=listVideoDescription

def jsonToContent(dictionary):
    #dictionary = json.load(open('template.json'))
    title = ""
    url =  ""
    content = ""
    description = ""
    containImage = False
    listImageDescription = []
    containVideo = False
    listVideoDescription = []
    content = ""
    contentSeparator= " "

    if 'title' in dictionary['page']:
        # use /0 to split Title and Content
        title = dictionary['page']['title']
        content = content + dictionary['page']['title'] +" "
    for cObject in dictionary['element']:
        cObjectType = cObject['type']
        if cObjectType == "cmultipletext":
            content = content + contentSeparator
            description = description + contentSeparator
            for contentData in cObject['content']:
                content = content + contentData + " "
                description = description + contentData + " "
            content = content + contentSeparator
            description = description + contentSeparator
        elif cObjectType == "crestable":
            for tableData in cObject['content']['value']:
                content = content + tableData['Award'] +contentSeparator + tableData['Member'] +contentSeparator +tableData['Date'] +contentSeparator
                description = description + tableData['Award'] +contentSeparator + tableData['Member'] +contentSeparator +tableData['Date'] +contentSeparator

        else:
            if 'content' in cObject:
                content = content + cObject['content'] + contentSeparator
                description = description + cObject['content'] + contentSeparator


        if 'alt' in cObject:
            content = content + cObject['alt'] + contentSeparator
            if cObjectType == "cvideo":
                containVideo= True
                listVideoDescription.append(cObject['alt'])
            else:
                containImage = True
                listImageDescription.append(cObject['alt'])


    tempDocument =  Document(-1,title,url,content,description,containImage,listImageDescription,containVideo,listVideoDescription)
    return tempDocument


def contentFromMysql():
    listOfContent = []
    mydb = mysql.connector.connect(
        host=config('host'),
        user=config('user'),
        password=config('password'),
        database=config('database'),
        port=config('port')
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sodsmain.page_rest_data WHERE sodsmain.page_rest_data.domain = \"public\" and sodsmain.page_rest_data.language = \"eng\" and sodsmain.page_rest_data.del_flag = 0;")
    myresult = mycursor.fetchall()
    index = 0
    for row in myresult:
        jsonData = json.loads(row[4])
        url = config('url') +str(row[2])
        finalContent =  jsonToContent(jsonData)
        finalContent.url = url
        finalContent.index = index
        if finalContent.url == (config('url')+"wordcrush"):
            finalContent.content += "Mini Game"
        index +=1
        listOfContent.append(finalContent)
    return  listOfContent

if __name__ == "__main__":
    #contentFromMysql()
    osystem = []
    osystem = contentFromMysql()
    for documentTest in osystem:
        print("============")
        print("Title is " + documentTest.title)
        print("Url is " + documentTest.url)
        print("Content is " + documentTest.content)
        print("Description is " + documentTest.description)
        print(" Contain video ? " + str(documentTest.containVideo))
        print("Video Description list ")
        print(*documentTest.listVideoDescription, sep=", ")
        print(" Contain image ? " + str(documentTest.containImage))
        print("Image Description list ")
        print(*documentTest.listImageDescription, sep=", ")
        print("===============")

