# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 20:33:32 2016

@author: antonio
"""
import itertools
from collections import OrderedDict
import pandas as pd
import re
import numpy

class Recommendation:
    #initialize_flags è la stringa di bit per il check dei 12 film. initialize_index rappresenta una lista di 12 numeri che indicano gli indici dei 12 film per l'assestamento iniziale dei gusti
    def __init__(self,initialize_flags, initialize_index):  
        self.movies_df = pd.read_csv('movies.csv',
                       names=['movie_id', 'movie_title', 'movie_genre'], encoding='latin-1')
        #Convertamo tutti i generi dei film in un set di variabili fittizie
        self.movies_df = pd.concat([self.movies_df, self.movies_df.movie_genre.str.get_dummies(sep='|')], axis=1) 
        #Siccome le categorie sono multiple, assegna a movie_categories tutte le colonne a partire dalla terza con lo slicing        
        self.movie_categories = self.movies_df.columns[3:]  
        
        #Lista degli indici dei film già proposti all utente per non riproporli
        self.seen = []
        #Inizializziamo i dizionari ordinati per il vettore delle preferenze e quello dei periodi usando la funzione zip che associa una lista vuota per ogni elemento di movie_categories. 
        self.user_preferences = OrderedDict(zip(self.movie_categories, []))
        self.user_period = OrderedDict(zip(self.movie_categories, []))
   
        #Inizializzazione dei generi e dei periodi nei dizionari ordinati usando come chiave le stringhe
        self.user_preferences['Action'] = 0  
        self.user_preferences['Adventure'] = 0  
        self.user_preferences['Animation'] = 0  
        self.user_preferences["Children's"] = 0  
        self.user_preferences["Comedy"] = 0  
        self.user_preferences['Crime'] = 0  
        self.user_preferences['Documentary'] = 0  
        self.user_preferences['Drama'] = 0  
        self.user_preferences['Fantasy'] = 0  
        self.user_preferences['Film-Noir'] = 0  
        self.user_preferences['Horror'] = 0  
        self.user_preferences['Musical'] = 0  
        self.user_preferences['Mystery'] = 0  
        self.user_preferences['Romance'] = 0  
        self.user_preferences['Sci-Fi'] = 0  
        self.user_preferences['War'] = 0 
        self.user_preferences['Thriller'] = 0  
        self.user_preferences['Western'] =0


        self.user_period['191'] = 0
        self.user_period['192'] = 0
        self.user_period['193'] = 0
        self.user_period['194'] = 0
        self.user_period['195'] = 0
        self.user_period['196'] = 0
        self.user_period['197'] = 0
        self.user_period['198'] = 0
        self.user_period['199'] = 0
        self.user_period['200'] = 0
        self.user_period['201'] = 0



        
        #ciclo la stringa di 0 e 1 ottenuta da javascript per vedere quali film sono stati selezionati dall'utente e ricevuti da flask 
        #utilizzo la tupla idx, i per poter avere l'elemento dentro i e l'indice del ciclo in idx attraverso enumerate
        for idx, i in enumerate(initialize_flags):
            # inserisco nella lista dei visti (seen) i film proposti tra i primi 12 così non mi vengono più proposti
            self.seen.append(initialize_index[idx])
            #controllo i flag settati con il carattere '1' e prendo solo questi in considerazione. 
            if i == '1':
                #ottengo il numero di generi attraverso il count degli elemtni della lista generata dallo split della stringa dei generi e quindi il numero dei generi. 
                n_genres = len( self.movies_df.loc[ initialize_index[idx] ][2].split('|') )
                #cicla ogni genere memorizzando il genere dentro j per ogni iterazione
                for j in self.movies_df.loc[ initialize_index[idx] ][2].split('|'):
                    #incrementa il valore del genere nel user_preferences dell'utente utilizzando come chiave la stringa del genere contenuta in j
                    self.user_preferences[j] = self.user_preferences[j] + float(1)/float(n_genres)


                #ottengo l'anno dal titolo sfruttando una regex ed estrapolo le prime tre cifre tramite slicing così da ottenere il decennio in tre cifre es. 199 per gli anni novanta
                period = re.search('([0-9][0-9][0-9][0-9])', self.movies_df.loc[ initialize_index[ idx ] ]['movie_title'] ).group(0)[:3]
                #utilizzo il decennio come chiave di stringa per il dizionario ordinato dei decenni e incremento il valore. 
                self.user_period[ period ] = self.user_period[ period ] + 1


    #metodo per aggiornare le preferenze di ogni utente via via che fa una scelta. Gli si passa l'id del film e il flag per capire se gli è piaciuto o no. Il flag viene dal si o dal no nel popup javascript
    def refresh_preferences (self, next_movie, like):
        #VEDERE SU 
        n_genres = len( self.movies_df.loc[int(next_movie)][2].split('|') )
        #cicla per ogni genere del film e controlla se il like dal javascript è 1 o 0. Se è 1 incrementa i valori del dizionario ordinato delle preferenze dei generi dell'utente
        #dividendo l'incremento per il numero di generi
        for j in self.movies_df.loc[next_movie][2].split('|'):
            if like == 1:
                self.user_preferences[j] = self.user_preferences[j] + float( (0 if self.user_preferences[j] >= 5 else 1) ) / float(n_genres)
            if like == 0:
                self.user_preferences[j] = self.user_preferences[j] - float( (0 if self.user_preferences[j] <= 0 else 1) ) / float(n_genres)
        #VEDERE SU


        self.seen.append(next_movie)
        #period = re.search('([0-9][0-9][0-9][0-9])', self.movies_df.loc[ next_movie ][ 'movie_title' ]).group(0)[:3]
        if like == 1:
            #qui controllo che l'intervallo sia sempre da 0 a 5
            self.user_period[ period ] = self.user_period[ period ] + (0 if self.user_period[ period ] >= 5 else 1)
        if like == 0:
            self.user_period[ period ] = self.user_period[ period ] - (0 if self.user_period[ period ] <= 0 else 1)
        

    #prodotto vettoriale fatto a mano. Prendo il punteggio del genere dai vettori passati dalle funzioni chiamanti e il vettore dei periodi dalle variabili globali
    def dot_product(self, vector_1, vector_2):  
        #calcolo il punteggio del genere come la somma di tutti gli elementi della lista risultante dal prodotto vettoriale dei due vettori
        genre_score = sum([ i*j for i,j in zip(vector_1, vector_2) ])
        period_score = sum([ i*j for i,j in zip(vector_1, self.user_period.values())])
        #restituisco la media tra i due putneggi. Valutare se fare una media ponderata valutando i coefficienti per determinare l'importanza di un parametro rispetto ad un altro. Periodo rispetto a genere
        return numpy.mean( [genre_score, period_score] )

    #semplice metodo di passaggio
    def get_movie_score(self, movie_features, user_preferences):
        return self.dot_product(movie_features, user_preferences)
    #questo metodo crea la colonna score nella struttura movies_df e gli applica il valore calcolato da get_movie_score e propone in maniera ordinata decrescente i film per punteggio
    #il parametro n_recommendations serve a determinare quanti film bisogna estrapolare dalla lista. a noi ne interessa solo uno e quindi prenderemo solo il primo che ha punteggio più alto
    def get_movie_recommendations(self, user_preferences, n_recommendations):  

        #aggiungiamo una colonna a movies_df con lo score calcolato per ogni film per un dato utente
        self.movies_df['score'] = self.movies_df[self.movie_categories].apply(self.get_movie_score, 
                                                           args=([self.user_preferences.values()]), axis=1)


        
        #si cicla il database ordinandolo in maniera decrescente per avere i film con maggior punteggio fino a quando non trova un film che non è nella lista seen e quindi che non è mai stato proposto
        #se non ci fosse uno scorrimento, verrebbe sempre proposto lo stesso film con il punteggio maggiore. per questo abbiamo introdotto la lista seen e applichiamo lo slicing per prendere un elemento solo
        #siamo costretti ad usare lo slicing per referenziare un solo elemento perchè altrimenti da problemi, DEBUGGARE
        for idx, i in enumerate(self.movies_df.sort_values(by=['score'], ascending=False)['movie_id'][:]):
            if i not in self.seen:
                print('\n')
                print(idx)
                print('\n')
                tmp_pandas_list = self.movies_df.sort_values(by=['score'], ascending=False)
                return {'id':tmp_pandas_list['movie_id'][idx:idx+1].values[0], 'title':tmp_pandas_list['movie_title'][idx:idx+1].values[0], 'genre':tmp_pandas_list['movie_genre'][idx:idx+1].values[0], 'genre_settings':self.user_preferences,'decade_settings':self.user_period }
                #return self.movies_df.sort_values(by=['score'], ascending=False)['movie_title'][idx:idx+1]
                

    #funzione che indica il prossimo film da cui estrarre il film consigliato
    def next_movie(self, movie_index, like):
        #l'indice del film sarà -1 solo nell inizializzazione delle preferenze per skippare la funzione di refresh_preferences. In tutti gli altri casi la funzione funzionerà
        if movie_index > -1:
            self.refresh_preferences(movie_index, like)
            #si ritorna la stringa del film proposto dal sistema di raccomandazione
        return self.get_movie_recommendations(self.user_preferences, 1)
    
#da scrivere se serve. In questo momento l'unico chiamante è flask. 
if __name__ == "__main__":
    pass



