__author__ = 'Lorenzo de la Paz'

from rank import score_BM25
import operator
    
class QueryProcessor:
    def __init__(self, logging, entidades, queries, tweets, tweetsConConsulta, frequenciesSubtema, 
                       frequenciesSubtemaEnTweets, terminosConsulta):
        self.logging = logging
        self.entidades = entidades
        self.queries = queries
        self.tweets = tweets
        self.tweetsConConsulta = tweetsConConsulta
        self.frequenciesSubtema = frequenciesSubtema
        self.frequenciesSubtemaEnTweets = frequenciesSubtemaEnTweets
        self.terminosConsulta = terminosConsulta
        #self.index, self.dlt = build_data_structures(corpus)

    def run(self):
        results = dict()
        
        #Por cada entidad
        for entidad in self.entidades:
            results[entidad] = self.run_query(entidad)
        return results

    def get_average_length(self, entidad):
        sum = 0
        for tweet in self.tweets[entidad]:
            length = len(tweet)
            sum += length
        #print('suma:',sum,'. tenemos un total de ',len(self.tweets[entidad]),' tweets')
        return float(sum) / len(self.tweets[entidad])

    def get_frequency_term_in_a_consult(self,terminosConsultaEntidad, idConsulta, subtema):
        sum = 0
        media = 0
        if idConsulta != '-1':
            print('idconsulta:',idConsulta,'\n')
            print('subtema',subtema,'\n')
            for termino in terminosConsultaEntidad[idConsulta]:
                #print(termino)
                if termino == subtema:
                    sum += 1
            print('aparece ',sum, 'y vamos a dividirlo por ',len(terminosConsultaEntidad[idConsulta]))
            print(sum / len(terminosConsultaEntidad[idConsulta]))
            media = sum / len(terminosConsultaEntidad[idConsulta])
            
        return media

    #FUNCION CON DUDAS - COMO REALIZAR EL PROCESAMIENTO
    def run_query(self, entidad):
        query_result = dict()
        frecuenciasDelSubtemaEntidad = self.frequenciesSubtema[entidad]
        frecuenciasDelSubtemaPorTweetEntidad = self.frequenciesSubtemaEnTweets[entidad]
        tweetsEntidad = self.tweets[entidad]
        tweetsConsultaEntidad = self.tweetsConConsulta[entidad]
        terminosConsultaEntidad = self.terminosConsulta[entidad]
        print('---------','Entidad ', entidad ,'---------')
        
        for subtema in frecuenciasDelSubtemaEntidad:
            print('----------','Subtema', subtema ,'---------')
            
            #print( frecuenciasDelSubtemaPorTweetEntidad[subtema])
            #print(frecuenciasDelSubtemaEntidad[subtema])
            #print(frecuenciasDelSubtemaPorTweetEntidad[subtema][tweet])
            #print(self.get_frequency_term_in_a_consult(terminosConsultaEntidad, consulta,subtema))
            if subtema in frecuenciasDelSubtemaPorTweetEntidad:
                for dupla in frecuenciasDelSubtemaPorTweetEntidad[subtema]:
                    #print(dupla)
                    for tweetTest in dupla:
                        frequencyTweetTest = dupla[tweetTest]
                        print('---------------','Tweet', tweetTest ,'---------')
                        query_result_tweet = dict()
                        idConsulta = tweetsConsultaEntidad[tweetTest]
                        print('Valores-- N:',int(frecuenciasDelSubtemaEntidad[subtema]), '. f: ', int(frequencyTweetTest), '. qfi:', self.get_frequency_term_in_a_consult(terminosConsultaEntidad, idConsulta, subtema), '. dl: ',len(tweetsEntidad[tweetTest]), '. avdl:', int(self.get_average_length(entidad)))
                        score = score_BM25(n=int(frecuenciasDelSubtemaEntidad[subtema]), f=int(frequencyTweetTest), qf=int(self.get_frequency_term_in_a_consult(terminosConsultaEntidad, idConsulta, subtema)),
                                      dl=len(tweetsEntidad[tweetTest]), avdl=int(self.get_average_length(entidad))) # calculate score
                    #score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=50000,
                    #                   dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length()) # calculate score
                        self.logging.info('Puntuación para la entidad ' + str(entidad) + ' con el par (subtema, tweet) (' + str(subtema) + ',' + str(tweetTest) + ') :' + str(score))
                        if subtema in query_result: #this document has already been scored once
                            query_result[subtema] += score
                        else:
                            query_result[subtema] = score
                #query_result[subtema] = query_result_tweet
            
        return query_result
    
    def run_classification(self, entidad):
        
        print('')
        