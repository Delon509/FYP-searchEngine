from marshmallow import Schema, fields
from pprint import pprint
import datetime as dt


class Website:
    def __init__(self, url,title,content):
        self.url = url
        self.title = title
        self.content = content


class WebsiteSchema(Schema):
    url = fields.String()
    title = fields.String()
    content = fields.String()


class OutputJson:
    def __init__(self, type, keyword,websites):
        self.type = type
        self.keyword = keyword # A User object
        self.created_at = dt.datetime.now()
        self.websites = websites


class OutputJsonSchema(Schema):
    type = fields.String()
    keyword = fields.List(fields.String())
    created_at = fields.DateTime()
    websites = fields.List(fields.Nested(WebsiteSchema()))


if __name__ == "__main__":
    website1 = Website(url="yahoo.com",title="Yahoo Search Engine",content="Over 2 people use our website")
    website2 = Website(url="youtube.com", title="Youtube", content="Hello Youtube!!")
    Websites = []
    Websites.append(website1)
    Websites.append(website2)
    json = OutputJson(type="question",keyword=["search,engine"],websites=Websites)
    author_result = OutputJsonSchema().dump(json)
    pprint(author_result, indent=2)