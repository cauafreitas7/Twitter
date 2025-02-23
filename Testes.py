import unittest 
from Twitter import Tweet, Perfil, PessoaFisica, PessoaJuridica, RepositoriosUsuarios, MyTwitter
from excecoes import UJCException

class TestTweet(unittest.TestCase):

    def Test_get_mensagem(self):
        perfil_teste = Perfil('user123')
        tweet_teste = Tweet(perfil_teste.get_usuario(), "Meu primeiro tweet!")
        self.assertEqual(perfil_teste.get_mensagem(), "Meu primeiro tweet!")
    
    def Test_get_id(self):
        perfil_teste = Perfil('user124')
        tweet_teste = Tweet(perfil_teste.get_usuario(), "Meu primeiro tweet!")
        self.assertEqual(perfil_teste.get_id(), 1)

    def Test_get_usuario(self):
        perfil_teste = Perfil('user125')
        tweet_teste = Tweet(perfil_teste.get_usuario(), "Meu primeiro tweet!")
        self.assertEqual(perfil_teste.get_usuario(), 'user125')

class TestPerfil(unittest.TestCase):

    def setUp(self):
        self.perfil1 = Perfil('usuario1')
        self.perfil2 = Perfil('usuario2')
        self.perfil3 = Perfil('usuario3')

        #Pessoa Físca
        self.pf1 = PessoaFisica('usuario1', '123.456.789-00')
        self.pf2 = PessoaFisica('usuario2', '987.654.321-00')

        #Pessoa Juridica
        self.pj1 = PessoaJuridica('PessoaJurica1', '12.345.678/0001-99')
        self.pj2 = PessoaJuridica('PessoaJuridica2', '98.765.432/0001-00')

    def test_add_seguidor(self):
        self.perfil1.add_seguidor(self.perfil2)
        self.assertIn(self.perfil2, self.perfil1._Perfil__seguidores)

    def test_add_seguidos(self):
        self.perfil1.add_seguidos(self.perfil2)
        self.assertIn(self.perfil2, self.perfil1._Perfil__seguidos)

    def test_add_tweet(self):
        tweet = Tweet('usuario1', 'Mensagem de teste')
        self.perfil1.add_tweet(tweet)
        self.assertIn(tweet, self.perfil1._Perfil__tweets)

    def test_get_tweets(self):
        # Adicionando tweets ao perfil1
        self.perfil1.add_tweet(self.tweet1)
        self.perfil1.add_tweet(self.tweet2)
        self.perfil1.add_tweet(self.tweet3)

        # Obtendo os tweets ordenados de perfil1
        tweets_ordenados = self.perfil1.get_tweets()

        # Comparando os atributos diretamente em vez de comparar os objetos
        self.assertEqual(tweets_ordenados[0].get_postagem(), self.tweet3.get_postagem())
        self.assertEqual(tweets_ordenados[1].get_postagem(), self.tweet1.get_postagem())
        self.assertEqual(tweets_ordenados[2].get_postagem(), self.tweet2.get_postagem())

    def test_get_tweets_com_vazio(self):
        # Teste para perfil vazio (sem tweets)
        tweets_ordenados = self.perfil2.get_tweets()
        self.assertEqual(tweets_ordenados, [])

    def test_get_tweet(self):
        tweet = Tweet('usuario1', 'Mensagem de teste')
        self.perfil1.add_tweet(tweet)
        tweet_recuperado = self.perfil1.get_tweet(tweet.get_id())
        self.assertEqual(tweet_recuperado, tweet)

    def test_get_timeline(self):
        tweet1 = Tweet('usuario1', 'Mensagem de teste 1')
        tweet2 = Tweet('usuario2', 'Mensagem de teste 2')
        self.perfil1.add_tweet(tweet1)
        self.perfil2.add_tweet(tweet2)
        self.perfil1.add_seguidos(self.perfil2)

        timeline = self.perfil1.get_timeline()
        self.assertIn(tweet2, timeline)
        self.assertIn(tweet1, timeline)

    def test_set_usuario(self):
        self.perfil1.set_usuario('novo_usuario')
        self.assertEqual(self.perfil1.get_usuario(), 'novo_usuario')

    def test_is_ativo(self):
        self.assertTrue(self.perfil1.is_ativo())
        self.perfil1.set_ativo(False)
        self.assertFalse(self.perfil1.is_ativo())

    def test_get_cpf(self):
        self.assertEqual(self.pf1.get_cpf(), '123.456.789-00')
        self.assertEqual(self.pf2.get_cpf(), '987.654.321-00')

    def test_get_cnpj(self):
        self.assertEqual(self.pj1.get_cnpj(), '12.345.678/0001-99')
        self.assertEqual(self.pj2.get_cnpj(), '98.765.432/0001-00')

class TestRepositoriosUsuarios(unittest.TestCase):

    def test_cadastrar_usuario(self):
        repo = RepositoriosUsuarios()
        perfil = Perfil("usuario1")
        repo.cadastrar(perfil)
        self.assertEqual(repo.buscar("usuario1"), perfil)
    
    def test_cadastrar_usuario_existente(self):
        repo = RepositoriosUsuarios()
        perfil = Perfil("usuario1")
        repo.cadastrar(perfil)
        with self.assertRaises(UJCException):
            repo.cadastrar(perfil)
    
    def test_atualizar_usuario(self):
        repo = RepositoriosUsuarios()
        perfil = Perfil("usuario1")
        repo.cadastrar(perfil)
        novo_perfil = Perfil("usuario1")
        repo.atualizar(novo_perfil)
        self.assertEqual(repo.buscar("usuario1"), novo_perfil)

class TestMyTwitter(unittest.TestCase):

    def setUp(self):
        self.my_twitter = MyTwitter()
        self.usuario1 = "@Zacarias"
        self.usuario2 = "@Catarina"
        self.usuario3 = "@Lucas"

    def test_criar_perfil(self):
        self.my_twitter.criar_perfil(self.usuario1)
        perfil = self.my_twitter._MyTwitter__repositorio.buscar(self.usuario1)
        self.assertEqual(perfil.usuario, self.usuario1)

    def test_cancelar_perfil(self):
        self.my_twitter.criar_perfil(self.usuario1)
        self.my_twitter.cancelar_perfil(self.usuario1)
        perfil = self.my_twitter._MyTwitter__repositorio.buscar(self.usuario1)
        self.assertEqual(perfil.is_ativo(), False)

    def test_tweetar(self):
        self.my_twitter.criar_perfil(self.usuario1)
        mensagem = "Meu primeiro tweet!"
        self.my_twitter.tweetar(self.usuario1, mensagem)
        perfil = self.my_twitter._MyTwitter__repositorio.buscar(self.usuario1)
        self.assertEqual(perfil.get_tweets()[-1].mensagem, mensagem)

    def test_seguir(self):
        self.my_twitter.criar_perfil(self.usuario1)
        self.my_twitter.criar_perfil(self.usuario2)
        self.my_twitter.seguir(self.usuario1, self.usuario2)
        perfil_seguidor = self.my_twitter._MyTwitter__repositorio.buscar(self.usuario2)
        self.assertEqual(self.usuario1 in perfil_seguidor.get_seguidores(), True)

if __name__ == "__main__":
    unittest.main()

