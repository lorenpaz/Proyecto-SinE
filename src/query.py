__author__ = 'Lorenzo de la Paz'

from rank import score_BM25
import operator
    
#Clase para el procesamiento principal de las consultas-subtemas
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
        self.precisionPorConsultaEntidad = dict()

    #Funcion que por cada entidad realiza el calculo
    def run(self):
        results = dict()
        
        #Por cada entidad
        for entidad in self.entidades:
            results[entidad] = self.run_query(entidad)
        return results

    #Funcion que calcula la media de los Tweets
    def get_average_length(self, entidad):
        sum = 0
        for tweet in self.tweets[entidad]:
            length = len(self.tweets[entidad][tweet])
            sum += length
        return float(sum) / len(self.tweets[entidad])

    #Funcion que calcula la frecuencia de un subtema en una consulta
    def get_frequency_term_in_a_consult(self,terminosConsultaEntidad, idConsulta, subtema):
        sum = 0
        media = 0
        if idConsulta != '-1':
            for termino in terminosConsultaEntidad[idConsulta]:
                if termino == subtema:
                    sum += 1

            media = sum / len(terminosConsultaEntidad[idConsulta])
            
        return media

    #Funcion que calcula la precision
    def calcular_precision(self, tweetsConsultaEntidad, tweetTest, consulta):
        idQuery = tweetsConsultaEntidad[tweetTest]
        
        if idQuery == consulta:
            return 1
        else:
            return 0
    
    def run_query(self, entidad):
    
        precisionPorConsulta = dict()
        frecuenciasDelSubtemaEntidad = self.frequenciesSubtema[entidad]
        frecuenciasDelSubtemaPorTweetEntidad = self.frequenciesSubtemaEnTweets[entidad]
        tweetsEntidad = self.tweets[entidad]
        tweetsConsultaEntidad = self.tweetsConConsulta[entidad]
        terminosConsultaEntidad = self.terminosConsulta[entidad]
        #print('---------','Fichero ', entidad ,'---------')
        
        query_result_consulta = dict()
        for consulta in terminosConsultaEntidad:
            #print('----------','Consulta ', consulta ,'---------')
            query_result_termino = dict()
            precision_tweet_consulta = dict()
            precision_tweet = dict()
            contadorDocumentosRelevantes = 0
            contadorDocumentosObtenidos = 0

            for terminoConsulta in terminosConsultaEntidad[consulta]:
                #print('terminoConsulta: ' + terminoConsulta)      

                if terminoConsulta in frecuenciasDelSubtemaPorTweetEntidad:
                    query_result_tweet = dict()
                    for dupla in frecuenciasDelSubtemaPorTweetEntidad[terminoConsulta]:
                        
                        #print('para el termino ', terminoConsulta,' tenemos la siguiente dupla: ',dupla)
                        for tweetTest in dupla:
                            contadorDocumentosObtenidos += 1
                            frequencyTweetTest = dupla[tweetTest]
                            
                            contadorDocumentosRelevantes += self.calcular_precision(tweetsConsultaEntidad, tweetTest, consulta)
                            
                            #print('---------------','Tweet ', tweetTest ,'---------')
                            #print('frequencyTweetTest: ',frequencyTweetTest)
                            #print('Valores-- N:',int(frecuenciasDelSubtemaEntidad[terminoConsulta]), '. f: ', int(frequencyTweetTest), '. qfi:', self.get_frequency_term_in_a_consult(terminosConsultaEntidad, consulta, terminoConsulta), '. dl: ',len(tweetsEntidad[tweetTest]), '. avdl:', int(self.get_average_length(entidad)))
                            score = score_BM25(n=int(frecuenciasDelSubtemaEntidad[terminoConsulta]), f=int(frequencyTweetTest), qf=self.get_frequency_term_in_a_consult(terminosConsultaEntidad, consulta, terminoConsulta),
                                          dl=len(tweetsEntidad[tweetTest]), avdl=int(self.get_average_length(entidad))) # calculate score
 
                            if tweetTest in query_result_termino: #this document has already been scored once
                                query_result_termino[tweetTest] += score
                            else:
                                query_result_termino[tweetTest] = score
                            
                            #print('precision para el tweet ',tweetTest,' : ',str(float(contadorDocumentosRelevantes) / float(contadorDocumentosObtenidos)))
                            precision_tweet = float(contadorDocumentosRelevantes) / float(contadorDocumentosObtenidos)
                            precision_tweet_consulta[tweetTest] = precision_tweet        

            query_result_consulta[consulta] = query_result_termino
            precisionPorConsulta[consulta] = precision_tweet_consulta
        self.precisionPorConsultaEntidad[entidad] = precisionPorConsulta
        #print('guardando en la consulta ',consulta, ' la precisión:',precision_tweet_consulta)
        return query_result_consulta
    
    #Funcion que calcula la precision de las Consultas-Tweets
    def run_classification(self):
        aver_prec = dict()
        for entidad in self.precisionPorConsultaEntidad:
            aver_prec_consulta = dict()

            for consulta in self.precisionPorConsultaEntidad[entidad]:
                sumatorio = 0
                contador = 0
                for tweet in self.precisionPorConsultaEntidad[entidad][consulta]:
                    sumatorio += self.precisionPorConsultaEntidad[entidad][consulta][tweet]
                    contador += 1
                if contador == 0:
                    average_precision = 0
                else:
                    average_precision = float(sumatorio) / float(contador)
                aver_prec_consulta[consulta] = average_precision
            aver_prec[entidad] = aver_prec_consulta
            
        return aver_prec