__author__ = 'Lorenzo de la Paz'

import re

#Clase para el parseo de los Tweets
class TweetsParser:

        def __init__(self):
                self.filenames = ['../Tweets/RL2013D01E001.dat', '../Tweets/RL2013D01E002.dat', '../Tweets/RL2013D01E003.dat', '../Tweets/RL2013D01E005.dat', '../Tweets/RL2013D01E008.dat', '../Tweets/RL2013D01E009.dat', '../Tweets/RL2013D01E012.dat', '../Tweets/RL2013D01E013.dat', '../Tweets/RL2013D01E014.dat', '../Tweets/RL2013D01E015.dat', '../Tweets/RL2013D01E016.dat', '../Tweets/RL2013D01E019.dat', '../Tweets/RL2013D01E022.dat', '../Tweets/RL2013D01E025.dat', '../Tweets/RL2013D01E033.dat', '../Tweets/RL2013D01E035.dat', '../Tweets/RL2013D01E040.dat',  '../Tweets/RL2013D01E041.dat',  '../Tweets/RL2013D01E043.dat',  '../Tweets/RL2013D01E044.dat']
                self.tweetsPorEntidad = dict()
                self.tweetsConsultaPorEntidad = dict()
            
        def parse(self):
                for file in self.filenames:
                        entidad = file[20:23]
                        #print(entidad)
                        with open(file, encoding='utf8') as f:
                                lines = '     '.join(f.readlines())
                        tweets = dict()
                        tweetsConConsulta = dict()
                        for x in lines.split('\n')[:-1]:
                                idTweet = x.split()[0]
                                textoTweet = ' '.join(x.split()[1:-1])
                                idQuery = x.rsplit()[-1]
                                #print(textoTweet)
                                #print(idTweet)
                                #print idQuery
                                tweets[idTweet] = textoTweet
                                tweetsConConsulta[idTweet] = idQuery
                                
                        self.tweetsPorEntidad[entidad] = tweets
                        self.tweetsConsultaPorEntidad[entidad] = tweetsConConsulta
        def get_tweets(self):
                return self.tweetsPorEntidad
        
        def get_tweets_entidad(self, entidad):
                if entidad in self.tweetsPorEntidad:
                        return self.tweetsPorEntidad[entidad]
                else:
                        return []

        def get_tweets_consulta(self):
                return self.tweetsConsultaPorEntidad
        
        def get_tweets_consulta_entidad(self, entidad):
                if entidad in self.tweetsConsultaPorEntidad:
                        return self.tweetsConsultaPorEntidad[entidad]
                else:
                        return []

#Clase para el parseo de las Consultas-Subtemas                    
class QueryParser:

        def __init__(self):
                self.filenames = ['../Queries/RL2013D01E001.dat', '../Queries/RL2013D01E002.dat', '../Queries/RL2013D01E003.dat', '../Queries/RL2013D01E005.dat', '../Queries/RL2013D01E008.dat', '../Queries/RL2013D01E009.dat', '../Queries/RL2013D01E012.dat', '../Queries/RL2013D01E013.dat', '../Queries/RL2013D01E014.dat', '../Queries/RL2013D01E015.dat', '../Queries/RL2013D01E016.dat', '../Queries/RL2013D01E019.dat', '../Queries/RL2013D01E022.dat', '../Queries/RL2013D01E025.dat', '../Queries/RL2013D01E033.dat', '../Queries/RL2013D01E035.dat', '../Queries/RL2013D01E040.dat',  '../Queries/RL2013D01E041.dat',  '../Queries/RL2013D01E043.dat',  '../Queries/RL2013D01E044.dat']
                self.terminosConsultaPorEntidad = dict()
                
        def parse(self):
                for file in self.filenames:
                        entidad = file[21:24]
                        #print(entidad)
                        with open(file, encoding='utf8') as f:
                                lines = '       '.join(f.readlines())
                        terminosConsulta = dict()
                        for x in lines.split('\n')[:-1]:
                                consulta = x.split()[0]
                                terminosDeLaConsulta = x.split()[1]
                                #print(terminosDeLaConsulta.strip().split(';'))
                                aux = terminosDeLaConsulta.split(';')
                                aux = [x for x in aux if x]
                                terminosConsulta[consulta] = aux
                        self.terminosConsultaPorEntidad[entidad] = terminosConsulta
                                        
        def get_terminosConsulta(self):
                return self.terminosConsultaPorEntidad
        
        def get_terminosConsulta_entidad(self, entidad):
                if entidad in self.terminosConsultaPorEntidad:
                        return self.terminosConsultaPorEntidad[entidad]
                else:
                        return []

#Clase para el parseo de las Frecuencias        
class FrequencyParser:

        def __init__(self):
                self.filenames = ['../Frecuencias/RL2013D01E001.dat', '../Frecuencias/RL2013D01E002.dat', '../Frecuencias/RL2013D01E003.dat', '../Frecuencias/RL2013D01E005.dat', '../Frecuencias/RL2013D01E008.dat', '../Frecuencias/RL2013D01E009.dat', '../Frecuencias/RL2013D01E012.dat', '../Frecuencias/RL2013D01E013.dat', '../Frecuencias/RL2013D01E014.dat', '../Frecuencias/RL2013D01E015.dat', '../Frecuencias/RL2013D01E016.dat', '../Frecuencias/RL2013D01E019.dat', '../Frecuencias/RL2013D01E022.dat', '../Frecuencias/RL2013D01E025.dat', '../Frecuencias/RL2013D01E033.dat', '../Frecuencias/RL2013D01E035.dat', '../Frecuencias/RL2013D01E040.dat',  '../Frecuencias/RL2013D01E041.dat',  '../Frecuencias/RL2013D01E043.dat',  '../Frecuencias/RL2013D01E044.dat']
                self.frecuenciaSubtemaPorEntidad = dict()
                self.frecuenciaSubtemaEnTweetsPorEntidad = dict()
        def parse(self):
                for file in self.filenames:
                        entidad = file[25:28]
                        #print(entidad)
                        with open(file, encoding='utf8') as f:
                                lines = '       '.join(f.readlines())
                        frecuenciaSubtema = dict()
                        frecuenciaSubtemaEnTweets = dict()
                        for x in lines.split('\n')[:-1]:
                                subtema = x.split()[0]
                                ocurrencias = x.split()[1]
                                frecuenciaSubtema[subtema] = ocurrencias
                                #print(subtema, ocurrencias)
                                if len(x.split()) > 2:
                                        listaDePares = x.split()[2]
                                        listaAcumulada = []
                                        for tupla in listaDePares.split(';'):
                                                #print(tupla)
                                                if len(tupla) > 1:
                                                        #print(tupla.split(',')[0])
                                                        #print(tupla.split(',')[1])
                                                        relacionTweetFrecuencia = dict()
                                                        relacionTweetFrecuencia[tupla.split(',')[0]] = tupla.split(',')[1]
                                                        listaAcumulada.append(relacionTweetFrecuencia)
                                        frecuenciaSubtemaEnTweets[subtema]  = listaAcumulada
                        self.frecuenciaSubtemaPorEntidad[entidad] = frecuenciaSubtema
                        self.frecuenciaSubtemaEnTweetsPorEntidad[entidad] = frecuenciaSubtemaEnTweets

        def get_frecuenciaSubtema(self):
                return self.frecuenciaSubtemaPorEntidad

        def get_frecuenciaSubtema_entidad(self, entidad):
                if entidad in self.frecuenciaSubtemaPorEntidad:
                        return self.frecuenciaSubtemaPorEntidad[entidad]
                else:
                        return []
                
        def get_frecuenciaSubtemaEnTweets(self):
                return self.frecuenciaSubtemaEnTweetsPorEntidad           

        def get_frecuenciaSubtemaEnTweets_entidad(self, entidad):
                if entidad in self.frecuenciaSubtemaEnTweetsPorEntidad:
                        return self.frecuenciaSubtemaEnTweetsPorEntidad[entidad]
                else:
                        return []
                
if __name__ == '__main__':
    
        #En los siguientes comentarios tenemos ejemplos de la obtención. 
        #Para ello, descomentar cada bloque y realizar las pruebas que se quieran.
        
        #fp = FrequencyParser()
        #fp.parse()
        #fs = fp.get_frecuenciaSubtema()
        #fst = fp.get_frecuenciaSubtemaEnTweets_entidad('001')
        #result = fst['way']
        #print(fst)

        #qp = QueryParser()
        #qp.parse()
        #qp = qp.get_terminosConsulta_entidad('001')
        #result = qp['1']
        #print(qp)

        tp = TweetsParser()
        tp.parse()
        terminosEntidadPrimera = tp.get_tweets_entidad('001')
        print(terminosEntidadPrimera['278797161079128064'])