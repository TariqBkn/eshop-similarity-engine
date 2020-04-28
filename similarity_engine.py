import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import my_db

class Similarity_engine:
    def __init__(self):
        self.db_connector=my_db.DB_connector()
        self.query = ""
        self.df=pd.DataFrame(columns=[" "])

    def get_similar_products_of(self, productId):
        self.load_products_in_dataframe()
        self.fill_na_in_dataframe()
        self.create_combined_features_column()
        # now convert a collection of text to a matrix of token counts
        count_matrix = CountVectorizer().fit_transform(self.df['combined_features'])
        # get the cosine similarity matrix from the count matrix 
        cosine_similarity_matrix = cosine_similarity(count_matrix)
        print(cosine_similarity_matrix)
        # Enumerate t hrough all the similarity scores of product with id==productId
        # to make a tuple of movie index similarity scores
        # we will return a list of tuples in form of (product id, similarity_score)
        similar_productId_similarityscore_pairs = list(enumerate(cosine_similarity_matrix[productId]))
        print(similar_productId_similarityscore_pairs)
        # sort the the list of similar products in descending order
        sorted_similar_productId_similarityscore_pairs =  sorted(similar_productId_similarityscore_pairs, key=lambda x:x[1], reverse=True)[1:]
        # key is the second element of the tuple which is similarity score
        # and we excluded the first element because it is the same product with a similarity score of 1
        print("--->",sorted_similar_productId_similarityscore_pairs)
        # We return the first 6 similar products
        return sorted_similar_productId_similarityscore_pairs[:6]
    def fill_na_in_dataframe(self):
        self.df.fillna(value="",inplace=True)

    def combine_features(self, row):
        return row['name']+" "+str(row['note'])+" "+row['provider_name']+" "+str(row['unit_price'])+" "+row['description']

    def create_combined_features_column(self):   
        self.df['combined_features'] = self.df.apply(self.combine_features, axis=1)

    def load_products_in_dataframe(self):
        self.query = "select * from product"
        self.mysql_cursor=self.db_connector.run_query(self.query)
        #num_fields = len(self.mysql_cursor.description)
        field_names = self.load_field_names_from_cursor()
        products = self.load_products_from_db()
        self.df = self.build_data_frame(products, field_names)
        
    def build_data_frame(self, products, field_names):
        df = pd.DataFrame(products, columns=field_names)
        return df

    def load_products_from_db(self):
        products=list()
        for row in self.mysql_cursor:
            products.append(row)
        return products

    def load_field_names_from_cursor(self):
        field_names = [i[0] for i in self.mysql_cursor.description]
        return field_names
