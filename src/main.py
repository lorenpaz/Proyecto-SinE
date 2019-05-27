__author__ = 'Lorenzo de la Paz'


from parse import *
from query import QueryProcessor
import operator
import os, platform, logging


def main():

    if platform.platform().startswith('Windows'):
        fichero_log = os.path.join(os.getenv('HOMEDRIVE'), 
                                   os.getenv("HOMEPATH"),
                                   'resultadosultimos.log')
    else:
        fichero_log = os.path.join(os.getenv('HOME'), 'resultadosultimos.log')
    
    print('Archivo Log en ', fichero_log)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s : %(levelname)s : %(message)s',
                        filename = fichero_log,
                        filemode = 'w')
    
    entidades = ['001' , '002', '003', '005', '008', '009', '012', '013', '014',
                 '015', '016', '019', '022', '025', '033', '035', '040', '041',
                 '043', '044']

    podium = 10

    qp = QueryParser()
    fp = FrequencyParser()
    tp = TweetsParser()
    
    qp.parse()
    fp.parse()
    tp.parse()
    
    queries = qp.get_terminosConsulta()
    tweets = tp.get_tweets()
    tweetsConConsulta = tp.get_tweets_consulta()
    frequenciesSubtema = fp.get_frecuenciaSubtema()
    frequenciesSubtemaEnTweets = fp.get_frecuenciaSubtemaEnTweets()
    terminosConsulta = qp.get_terminosConsulta()
    proc = QueryProcessor(logging, entidades, queries, tweets, tweetsConConsulta, frequenciesSubtema, 
                       frequenciesSubtemaEnTweets, terminosConsulta)
    results = proc.run()

    for entidad in results:
        tmpPrincipal = ('----------' + 'Fichero: ' + str(entidad) + '----------')
        #print(tmpPrincipal)
        logging.info(tmpPrincipal)
        for consulta in results[entidad]:
            
            #Ordenamos por el valor (score)
            sorted_x = sorted(results[entidad][consulta].items(), key=operator.itemgetter(1))
            sorted_x.reverse()
            
            #Posicion
            index = 1
            tmpSecundario = ('-----' + 'Consulta: ' + str(consulta) + '-----' + '\n' + '----- Las '+str(podium)+' mejores posiciones -----')
            #print(tmpSecundario)
            logging.info(tmpSecundario)
            
            #Buscamos los 10 tweets más relevantes
            for i in sorted_x[:podium]:
                tmp = ('-- Posicion ' + str(index) + ' -- Tweet: ' + str(i[0]) + ' con puntuacion: ' + str(i[1]) + ' -- ')
                #print(tmp)
                logging.info(tmp)
                index += 1
    
    resultsPrecision = proc.run_classification()
    tmpPrincipal = ('--------------- Precisiones---------------')
    #print(tmpPrincipal)
    logging.info(tmpPrincipal)
        
    for entidad in resultsPrecision:
        tmpPrincipal = ('----------' + 'Fichero: ' + str(entidad) + '----------')
        #print(tmpPrincipal)
        logging.info(tmpPrincipal)
        
        for consulta in resultsPrecision[entidad]:
            tmpSecundario = ('-----' + 'Precisión para la consulta: ' + str(consulta) +' : ' +str(resultsPrecision[entidad][consulta])+' -----')
            #print(tmpSecundario)
            logging.info(tmpSecundario)

if __name__ == '__main__':
    main()