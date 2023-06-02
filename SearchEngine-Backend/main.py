import pickle
from OutputJson import *
from getContent import contentFromMysql
from invertedIndex import *
import pandas as pd
from flask import Flask, request
import yake
import json
from txtai.embeddings import Embeddings
from flask_cors import CORS, cross_origin


def generateErrorResponse(reason):
    error_response = {
        "HTTP status": 403,
        "Reason": reason,

    }
    return json.dumps(error_response)
# Create embeddings model, backed by sentence-transformers & transformers
#embeddings = Embeddings({"path": "sentence-transformers/nli-mpnet-base-v2"})
data = ["US tops 5 million confirmed virus cases",
            "Canada's last fully intact ice shelf has suddenly collapsed, forming a Manhattan-sized iceberg",
            "Beijing mobilises invasion craft along coast as Taiwan tensions escalate",
            "The National Park Service warns against sacrificing slower friends in a bear attack",
            "Maine man wins $1M from $25 lottery ticket",
            "Make huge profits without work, earn up to $100,000 a day"]
#embeddings.index([(uid, text, None) for uid, text in enumerate(data)])
#embeddings.save("index")
print("saved embedding")
def getKeyword(string):
    kw_extractor = yake.KeywordExtractor()
    listofKeyword= []
    language = "en"
    max_ngram_size = 5
    deduplication_threshold = 0.1
    numOfKeywords = 5
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(string)
    for kw in keywords:
        print(kw[0])
        listofKeyword.append(kw[0])
    return  listofKeyword


with open('finalized_model.pkl', 'rb') as f:
    vectorizer, naive_bayes = pickle.load(f)

#app = Flask(__name__, static_folder='../build', static_url_path='/')
app = Flask(__name__)
CORS(app)
#Get List of Document Object From Mysql
#Documents = contentFromMysql() <- Change Sql statement before uncomment

#Below Documents Object is  For Test Front End
# D1 =  Document(0,"Football - Wikipedia","https://en.wikipedia.org/wiki/Football","Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. Unqualified, the word football normally means the form of football that is the most popular where the word is used. Sports commonly called football include association football (known as soccer in North America and Australia);"
#                ,"Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. · There are a number of references to traditional, ancient, ...",True,["shoot","world cup"],False,[])
# D2 =  Document(1,"Basketball - Wikipedia","https://en.wikipedia.org/wiki/Basketball","Basketball is a team sport in which two teams, most commonly of five players each, opposing one another on a rectangular court, compete with the primary objective of shooting a basketball (approximately 9.4 inches (24 cm) in diameter) through the defender's hoop (a basket 18 inches (46 cm) in diameter mounted 10 feet (3.048 m) high to a backboard at each end of the court, while preventing the opposing team from shooting through their own hoop."
#                ,"Basketball is a team sport ; Players advance the ball by bouncing it while walking or running (dribbling) or by passing it to a teammate, both of which require ...",False,[],True,["NBA", "Michael Jordan"])
# D3 =  Document(2,"Rice - Wikipedia","https://en.wikipedia.org/wiki/Rice","Rice is the seed of the grass species Oryza sativa (Asian rice) or less commonly Oryza glaberrima (African rice). The name wild rice is usually used for species of the genera Zizania and Porteresia, both wild and domesticated, although the term may also be used for primitive or uncultivated varieties of Oryza.",
#                "Rice is the seed of the grass species Oryza sativa (Asian rice) or less commonly Oryza glaberrima (African rice). The name wild rice is usually used for ...",False,[],False,[])
# D4 =  Document(3,"Noodle - Wikipedia","https://en.wikipedia.org/wiki/Noodle","Noodles are usually cooked in boiling water, sometimes with cooking oil or salt added. They are often pan-fried or deep-fried. Noodles are often served with an accompanying sauce or in a soup. Noodles can be refrigerated for short-term storage or dried and stored for future use.",
#                "Noodles are a type of food made from unleavened dough which is either rolled flat and cut, stretched, or extruded, into long strips or strings.",False,[],False,[])
# D5 =  Document(4,"Pizza - Wikipedia","https://en.wikipedia.org/wiki/Pizza","In 2017, the world pizza market was US$128 billion, and in the US it was $44 billion spread over 76,000 pizzerias.",
#                "Pizza is a dish of Italian origin consisting of a usually round, flat base of leavened wheat-based dough topped with tomatoes, cheese, and often various ...",True,["pizza with ice cream"],False,[])
# D6 =  Document(5,"Bread - Wikipedia","https://en.wikipedia.org/wiki/Bread","Bread is a staple food prepared from a dough of flour (usually wheat) and water, usually by baking. Throughout recorded history and around the world, it has been an important part of many cultures' diet. It is one of the oldest human-made foods, having been of significance since the dawn of agriculture, and plays an essential role in both religious rituals and secular culture.",
#                "Bread is a staple food prepared from a dough of flour (usually wheat) and water, usually by baking. Throughout recorded history and around the world, ...",True,["white bread"],True,"baking bread")
# D7 =  Document(6,"Ice cream - Wikipedia","https://en.wikipedia.org/wiki/Ice_cream","Ice cream is a sweetened frozen food typically eaten as a snack or dessert. It may be made from milk or cream and is flavoured with a sweetener, either sugar or an alternative, and a spice, such as cocoa or vanilla, or with fruit such as strawberries or peaches. It can also be made by whisking a flavored cream base and liquid nitrogen together. ",
# "Ice cream is a sweetened frozen food typically eaten as a snack or dessert. It may be made from milk or cream and is flavoured with a sweetener, ...",False,[],False,[])
# D8 =  Document(7,"Watermelon - Wikipedia","https://en.wikipedia.org/wiki/Watermelon","Watermelon (Citrullus lanatus) is a flowering plant species of the Cucurbitaceae family and the name of its edible fruit. A scrambling and trailing vine-like plant, it is a highly cultivated fruit worldwide, with more than 1,000 varieties.",
#                "Watermelon (Citrullus lanatus) is a flowering plant species of the Cucurbitaceae family and the name of its edible fruit. A scrambling and trailing ...",True,["green"],False,[])
# Documents = [D1,D2,D3,D4,D5,D6,D7,D8]
Documents = contentFromMysql()
textContent = []
videoContent = []
imageContent = []




for document in Documents:
    textContent.append(document.content)
    if document.containVideo == True:
        videoString = ""
        for temp in document.listVideoDescription:
            videoString += temp
        videoContent.append(videoString)
    if document.containImage == True:
        imageString = ""
        for temp in document.listVideoDescription:
            imageString += temp
        imageContent.append(imageString)
embeddings = Embeddings()
# embeddings.index([(uid, text, None) for uid, text in enumerate(textContent)])
# embeddings.save("text")
# embeddings.index([(uid, text, None) for uid, text in enumerate(videoContent)])
# embeddings.save("video")
# embeddings.index([(uid, text, None) for uid, text in enumerate(imageContent)])
# embeddings.save("image")



@app.route("/api/search", methods=['POST'])
@cross_origin()
def hello_world():
    searchContent = []
    inRangeDocument = []
    Reason = ""
    responseType = "statement"
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        if('query' not in data):
            return generateErrorResponse("Missing Query")
        if ('type' not in data):
            return generateErrorResponse("Missing Type")
        print(data)

        query = data['query']
        keywords = getKeyword(query)
        print("keywords is " )
        print(*keywords , sep=", ")
        print("User Provide Correct Json")
        #Check Query is statement or question
        df_query = pd.DataFrame({'doc': [query]})
        if naive_bayes.predict(vectorizer.transform(df_query['doc'])) == [1]:
            responseType = "question"
            print("the response type is question")
        type = data['type']
        if( type != 'text' and type !='video' and type !='image'):
            return generateErrorResponse("Type should be text/video/image")
        if responseType == "statement":
            if query not in keywords:
                keywords.append(query)
            print("We add the query to statement")

        # Base on the type , Change Embedding model , Search Content
        if( type == 'text'):
            print("The incoming json type is text")
            embeddings.load("text")
            searchContent = textContent
            for document in Documents:
                inRangeDocument.append(document)

        elif (type == "video"):
            print("The incoming json type is video")
            embeddings.load("video")
            searchContent = videoContent
            for document in Documents:
                if document.containVideo == True :
                    inRangeDocument.append(document)

        else:
            print("The incoming json type is image")
            embeddings.load("image")
            searchContent = imageContent
            for document in Documents:
                if document.containImage == True:
                    inRangeDocument.append(document)
        print("after three type cases")
        inverted = {}
        inverted_documents = {}
        for x in range(len(searchContent)):
            inverted_documents[x] = searchContent[x]
        for doc_id, text in inverted_documents.items():
            doc_index = inverted_index(text)
            inverted_index_add(inverted, doc_id, doc_index)
        possibleCandidate = {}
        for x in range(len(textContent)):
            possibleCandidate[x] = 0
        for keyword in keywords:
            uid = embeddings.search(keyword, 1)[0][0]
            #print("Embedding choose the  title is "+ inRangeDocument[uid].title)
            possibleCandidate[inRangeDocument[uid].index] +=1
            result_docs = search(inverted, keyword)
            for result in result_docs:
                possibleCandidate[inRangeDocument[result].index]+=1
                #print("Inverted choose the  title is " + inRangeDocument[result].title)
        print("Finish searching")
        #for k, v in possibleCandidate.items():
            #print("The key is " +inRangeDocument[k].title)
            #print("The value is" + str(v))
        largest = sorted(((v, k) for k, v in possibleCandidate.items()))
        Websites = []
        for x in range(3):
            if x<= len(possibleCandidate) and largest[-x][0]>0:
                current = Documents[largest[-x][1]]
                temp_website = Website(url=current.url , title= current.title , content= current.description )
                Websites.append(temp_website)
        response = OutputJson(type=responseType, keyword=keywords, websites=Websites)
        return OutputJsonSchema().dump(response)
    else:
        return generateErrorResponse("Invalid Content Type")






if __name__ == "__main__":

    app.run(debug=True)
    #querys = pd.DataFrame({'doc': ["In what country is the Edwards Campus located"]})
    #print(query)
    #print(naive_bayes.predict(vectorizer.transform(querys)))
    #if naive_bayes.predict(vectorizer.transform(querys)) == [1] :
        #print("Question")

    #store =getKeyword("In German, there is no apple to eat")
    #print(store)





    #embeddings = Embeddings()
    #embeddings.load("index")
    #uid = embeddings.search(",gpl's,kdgpkp", 1)[0][0]
    #print(data[uid])
