# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import sqlalchemy as db
from aws.settings import DATABASE_PASSWORD,DATABASE_USER,DATABASE_IP,DATABASE_NAME
from pprint import pprint

def clean(s):
    if s:
        s = re.sub(' {2,}', ' ', s)
        s = s.replace('\n','')
        s = s.replace('\r','')
    return s


class PeoplePipeline(object):
    items =0

    def __init__(self):

        engine = db.create_engine(
            f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_IP}"
        )
        self.connection = engine.connect()

        if DATABASE_NAME not in self.connection.dialect.get_schema_names(self.connection):
            engine.execute(db.schema.CreateSchema(DATABASE_NAME))
        self.connection.execute(f"use {DATABASE_NAME};")
        metadata = db.MetaData(schema=DATABASE_NAME)
        tables = [i[0] for i in self.connection.execute('show tables;').fetchall()]

        self.AISNs = db.Table('AISNs', metadata,
                         db.Column('id', db.Integer(), autoincrement=True, primary_key=True),
                         db.Column('AISN', db.String(255), nullable=False, unique=True),
                         )
        if 'AISNs' not in tables:
            metadata.create_all(engine, tables=[self.AISNs])

        self.product_info = db.Table('product_info', metadata,
                                db.Column('id', db.Integer(), autoincrement=True, primary_key=True),
                                db.Column('AISN', db.String(100), nullable=False),
                                db.Column('title', db.String(255), nullable=False),
                                db.Column('url', db.String(255), nullable=False),
                                db.Column('average_rating', db.Float()),
                                db.Column('total_rating', db.Integer()),
                                db.Column('questions_answered', db.Integer()),
                                )
        if 'product_info' not in tables:
          metadata.create_all(engine, tables=[self.product_info])

        self.reviews = db.Table('reviews', metadata,
                           db.Column('id', db.Integer(), autoincrement=True, primary_key=True),
                           db.Column('AISN', db.String(255), nullable=False),
                           db.Column('positive_reviews', db.Float()),
                           db.Column('critical_reviews', db.Integer()),
                           db.Column('total_reviews', db.Integer()),
                           )

        if 'reviews' not in tables:
            metadata.create_all(engine, tables=[self.reviews])

    def process_item(self, item, spider):
        for k,v in item.items():
            item[k]=clean(v)
        item['Average rating']=float(item['Average rating'].split()[0])
        item['Total ratings']=int(item['Total ratings'].split()[0].replace(',',''))
        try:
            item['Questions answered']=int([i for i in item['Questions answered'].split() if i[0].isdigit()][0].replace(',',''))
        except AttributeError:
            item['Questions answered'] =0
        try:
            item['Positive reviews']=int(item['Positive reviews'].split()[2].replace(',',''))
        except AttributeError:
            item['Positive reviews'] = 0
        try:
            item['Critical reviews']=int(item['Critical reviews'].split()[2].replace(',',''))
        except AttributeError:
            item['Critical reviews'] = 0
        try:
            item['Total reviews']=int(item['Total reviews'].split()[-2].replace(',',''))
        except AttributeError:
            item['Total reviews'] = 0

        self.connection.execute(db.insert(self.AISNs) ,
                                {'AISN':item['AISN']})

        self.connection.execute(db.insert(self.product_info) ,
                                {'AISN':item['AISN'],
                                 'url':item['URL'],
                                 'title':item['Title'],
                                 "average_rating":item['Average rating'],
                                 "total_rating":item['Total ratings'],
                                 'questions_answered':item['Questions answered']
                                                                       })
        self.connection.execute(db.insert(self.reviews) ,
                                {'AISN':item['AISN'],
                                 "positive_reviews":item['Positive reviews'],
                                 "critical_reviews": item['Critical reviews'],
                                 'total_reviews':item['Total reviews']})
        pprint(item)

        return item




