import datetime
from funcoes_aux import gerador
from excecoes import UJCException, UNCException, PPException, PDException, PIException, MFPException, SIException

class Tweet:

    def __init__(self, nome_usuario:str, texto:str, gerador):
        self.__usuario = nome_usuario
        self.__mensagem = texto 
        self.__id = next(gerador)
        self.__data_postagem = datetime.now()

    def get_id(self):
        return self.__id
    
    def get_usuario(self):
        return self.__usuario
    
    def get_mensagem(self):
        return self.__mensagem
    
    def get_data_postagem(self):
        return self.__data_postagem 

class Perfil():
    def __init__(self, usuario:str):
        self.__usuario = usuario
        self.__seguidos = []
        self.__seguidores = []
        self.__tweets = []
        self.__ativo = True

    def add_seguidor(self, perfil):
        self.__seguidores.append(perfil)

    def add_seguidos(self, perfil):
        self.__seguidos.append(perfil)

    def add_tweet(self, tweet):
        self.__tweets.append(tweet)

    def get_tweets(self):
        return sorted(self.__tweets, key=lambda t: t.get_postagem(), reverse=True)

    def get_tweet(self, tweet_id):
        for tweet in self.__tweets:
            if tweet.get_id() == tweet_id:
                return tweet
        return None

    def get_timeline(self):
        timeline = self.__tweets[:]
        for perfil in self.__seguidos:
            timeline.extend(perfil.get_tweets())
        return sorted(timeline, key=lambda t: t.get_postagem())

    def set_usuario(self, usuario):
        self.__usuario = usuario

    def get_usuario(self):
        return self.__usuario

    def set_ativo(self, ativo: bool):
        self.__ativo = ativo

    def is_ativo(self):
        return self.__ativo

    def get_seguidores(self):
        return self.__seguidores

    def get_seguidos(self):
        return self.__seguidos

class PessoaFisica(Perfil):
    def __init__(self, usuario, cpf):
        super().__init__(usuario)
        self.__cpf = cpf

    def get_cpf(self):
        return self.__cpf

class PessoaJuridica(Perfil):
    def __init__(self, usuario, cnpj):
        super().__init__(usuario)
        self.__cnpj = cnpj

    def get_cnpj(self):
        return self.__cnpj

class RepositoriosUsuarios():
    def __init__(self):
        self.__usuarios = []
    
    def cadastrar(self, perfil: Perfil):
        if self.buscar(perfil.get_usuario()) is not None:
            raise UJCException(perfil.get_usuario())
        self.__usuarios.append(perfil)
    
    def buscar(self, usuario):
        for perfil in self.__usuarios:
            if perfil.get_usuario() == usuario:
                return perfil
        return None
    
    def atualizar(self, perfil: Perfil):
        usuario = self.buscar(perfil.get_usuario())
        if usuario is None:
            raise UNCException(perfil.get_usuario())
        else:
            self.__usuarios.remove(usuario)
            self.__usuarios.append(perfil)

class MyTwitter:
    def __init__(self):
        self.__repositorio = RepositoriosUsuarios()
    
    def criar_perfil(self, usuario):
        perfil = self.__repositorio.buscar(usuario)

        if perfil is not None:
            raise PEException(usuario)
        self.__repositorio.cadastrar(perfil)

    def cancelar_perfil(self, usuario):
        perfil = self.__repositorio.buscar(usuario)

        if perfil is None:
            raise PIException(usuario)
        elif perfil is not None and perfil.is_ativo() == False:
            raise PDException(usuario)
        else:
            perfil.set_ativo(False)


    def tweetar(self, usuario, mensagem):
        perfil = self.__repositorio.buscar(usuario)
        
        if perfil is None or perfil.is_ativo() == False:
            raise PIException(usuario)
        elif len(mensagem) < 1 or len(mensagem) > 140:
            raise MFPException(usuario) 
        else:
            tweet = Tweet(usuario, mensagem)
            perfil.add_tweet(tweet)

    def timeline(self, usuario):
        perfil = self.__repositorio.buscar(usuario)

        if perfil is None: 
            raise PIException(usuario)
        elif perfil is not None and perfil.is_ativo() == False:
            raise PDException(usuario)
        else: 
            perfil.get_timeline()

    def tweets(self, usuario):
        perfil = self.__repositorio.buscar(usuario)

        if perfil is None:
            raise PIException(usuario)
        elif perfil is not None and perfil.is_ativo() == False:
            raise PDException(usuario)
        else:
            perfil.get_tweets()

    def seguir(self, usuario_seguido, usuario_seguidor):
        perfil_seguido = self.__repositorio.buscar(usuario_seguido)
        perfil_seguidor = self.__repositorio.buscar(usuario_seguidor)

        if perfil_seguido is None or perfil_seguidor is None:
            raise PIException(usuario)
        elif perfil_seguido.is_ativo() == False or perfil_seguidor.is_ativo() == False:
            raise PDException(usuario)
        else:
            perfil_seguido.add_seguidor(perfil_seguidor)
            perfil_seguidor.add_seguidos(perfil_seguido)

    def numero_seguidores(self, usuario):
        perfil = self.__repositorio.buscar(usuario)

        if perfil is None:
            raise PIException(usuario)
        elif perfil is not None and perfil.is_ativo() == False:
            raise PDException(usuario)
        else:
            count = 0
            for seguidor in perfil.seguidores():
                seguidor = self.__repositorio.buscar(seguidor)
                if seguidor is not None and seguidor.is_ativo():
                    count += 1
            return count
    
    def seguidores(self):
        perfil = self.__repositorio.buscar(usuario)

        if perfil is None: 
            raise PIException(usuario)
        elif perfil is not None and perfil.is_ativo() == False:
            raise PDException(usuario)
        else:
            list_seguidores = []
            for seguidor in perfil.seguidores():
                seguidor = self.__repositorio.buscar(seguidor)
                if seguidor is not None and seguidor.is_ativo() == True:
                    list_seguidores.append(seguidor)
            return list_seguidores

    def seguidos(self):
        perfil = self.__repositorio.buscar(usuario)
        
        if perfil is None: 
            raise PIException(usuario)
        elif perfil is not None and perfil.is_ativo() == False:
            raise PDException(usuario)
        else:
            list_seguidos = []
            for seguido in perfil.seguidos():
                seguido = self.__repositorio.buscar(seguido)
                if seguido is not None and seguido.is_ativo() == True:
                    list_seguido.append(seguido)
            return list_seguido

