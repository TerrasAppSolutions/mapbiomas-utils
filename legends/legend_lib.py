import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras
import config


def add_nivel(df):
    """
        The function should add a column showing 
        a number of the level of hierarchy
    """

    def get_next_level(parent, nivel):
        if parent == 0:
            return nivel
        
        parent_level = df.loc[df['id']==parent,'nivel'].values[0]
        
        next_level = None        
        if parent_level:
            next_level = parent_level + 1
        return next_level


    df['nivel'] = None

    df.loc[df.parent == 0, 'nivel'] = 1
    df['nivel'] = df.apply(lambda x: get_next_level(x['parent'], x['nivel']), axis=1)
    df['nivel'] = df.apply(lambda x: get_next_level(x['parent'], x['nivel']), axis=1)
    df['nivel'] = df['nivel'].astype(int)


def add_valor(df):

    def get_valor_l1_for_l3(x):
        r = df['parent'].loc[(df['id'] == x['valor_l2']) & (df['nivel'] == 2)].values
        r = r[0] if r else None
        return r


    df['valor'] = None
    df['valor_l1'] = None
    df['valor_l2'] = None
    df['valor_l3'] = None

    df['valor'] = df['id']


    #level 1
    df['valor_l1'] = df['id'].where(df['nivel'] == 1, df['valor_l1'])
    df['valor_l2'] = df['id'].where(df['nivel'] == 1, df['valor_l2'])
    df['valor_l3'] = df['id'].where(df['nivel'] == 1, df['valor_l3'])

    
    #level 2
    df['valor_l1'] = df['parent'].where(df['nivel'] == 2, df['valor_l1'])
    df['valor_l2'] = df['id'].where(df['nivel'] == 2, df['valor_l2'])
    df['valor_l3'] = df['id'].where(df['nivel'] == 2, df['valor_l3'])

    #level 3    
    f = lambda x: df['parent'].loc[(df['valor_l2'] == x['valor_l2']) & (df['nivel'] == 2)]
    
    df['valor_l2'] = df['parent'].where(df['nivel'] == 3, df['valor_l2'])
    df['valor_l1'] = np.where(df['nivel'] == 3, df.apply(get_valor_l1_for_l3, axis=1), df['valor_l1'])
    df['valor_l3'] = df['id'].where(df['nivel'] == 3, df['valor_l3'])

def rename_col(df):
    df.rename(columns={"parent": "parente"}, inplace=True)

def adjust_data(path, versao=None):
    df = pd.read_csv(path, sep=",")
    df.dropna(inplace=True, subset=['id', 'parent', 'cor'])

    df['versao'] = versao

    df['ativo'] = df['ativo'].apply(lambda x: bool(x))

    add_nivel(df)  

    add_valor(df)

    rename_col(df)

    return list(df.T.to_dict().values())

