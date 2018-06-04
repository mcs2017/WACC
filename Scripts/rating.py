import numpy as np
import pandas as pd
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob import protocol
import csv
################################################################################
# python3 rating.py --jobconf mapreduce.job.reduces=1 new_neighbor_500_6.txt.csv
################################################################################

class MRAverage(MRJob):

    def mapper_init(self):
        self.df = pd.read_csv('price_star.csv', sep=",")

    def mapper(self, _, line):
        line = np.array(line.split(',')) 
        id1, id2 = line[0], line[1]
        rating2 = float(self.df[self.df['business_id'] == id2]['stars'])
        if rating2 is not None:
            yield id1, rating2
    
    def reducer(self, key, value):
        sum_rating = 0
        count = 0
        for i in value:
            sum_rating += i
            count += 1
        if count != 0:
            yield key, sum_rating/count


if __name__ == '__main__':
    MRAverage.run()