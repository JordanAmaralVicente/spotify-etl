# Spotify ETL tracked songs
Um simples projeto em python que vai buscar as músicas ouvidas nas últimas 24 horas do seu spotify, vai verificar e validar os dados e depois disso vai colocar em um banco de dados SQLITE.

## Tokens
Para fazer a conexao com o spotify é necessário de um token de acesso que pode ser obtido no seguinte link: [Get recently played](https://developer.spotify.com/console/get-recently-played/) . 
Esse token é temporário, então ele tem um data de expiração que se não me engano são 10 minutos. Para gerar o token, você acessa o link, clica em get token, se for a primeira vez, ele pedirá acesso a conta, da segunda vez ele não pedirá mais, após isso você clica na primeira checkbox que aparece e após isso é só gerar o token. 

Uma vez gerado o token, basta ir no main.py e susbtituir o TOKEN e seu USER_ID

## Próximos passos
Pretendo implementar o refresh token authetication. Porém caso eu faça isso, o código não será disponibilizado por haver chaves secretas. Em vez disso, disponibilizarei através de interfce gráfica.

## Considerações
Não foi eu quem desenvolvi isso do zero. O crédito é todo de Karolina Sowinska que você pode encontrar através do canal no [Youtube](https://www.youtube.com/channel/UCAxnMry1lETl47xQWABvH7g)
