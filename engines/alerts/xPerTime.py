
import elasticsearch
from elasticsearch_dsl import Search, Q
from datetime import datetime

class xpertime:
    def __init__(self, conns, args):
        self.config = args
        self.conns = conns
        self.count = args["count"]

    def run(self,alertConfig):
        #print alertConfig
        indexTimestamp = alertConfig["index"].split("+")[-1]
        query = alertConfig["query"]
        timeFrame = alertConfig["timeframe"]
        time = datetime.now()
        date = time.strftime(indexTimestamp)
        index = alertConfig["index"].replace("]+"+indexTimestamp,date).replace("[", "")
        #print index
        try:
            client = elasticsearch.Elasticsearch(self.conns)
            s = Search(using=client, index=index).filter({"range": {"@timestamp": {"gt": "now-"+timeFrame}}})
            #print s.to_dict()
            response = s.execute()
        except elasticsearch.exceptions.NotFoundError as error:
            print "Index %s not found" % (index)
        else:
            count = 0
            for i in response:
                #print i["@timestamp"]
                count += 1
            if count >= self.count:
                print "Alert"
                return
            print "Fine"

def init(conns, args):
    return xpertime(conns, args)
