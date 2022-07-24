<p align="center"><img src="https://user-images.githubusercontent.com/59841892/172259927-c8463fb8-64b4-4490-beca-bd8ac044a693.png" style="max-width: 100%;"></p>
<h1 align="center"> gerador de sequencia </h1>
<p>
  usado para gerar sequencias aleatória pro jogo da mega sena, os filtros se baseam em estatistica e probabilidade.
  Uma sequencia aleatória é gerada e então é passada pelos filtros escolhidos, as sequencias permitidas serão mostrada ao usuario.
</p>
<p>as sequencias não são retiradas da internet, para que funcione mesmo offline</p>
<h1> Os filtros são: </h1>
<ol>
  <li> filtro: retira os numeros das 3 ultimas sequencias da mega sena
  <li> filtro: retira a sequencia se tiver mais que dois intervalos igual, se tiver mais que 4 impares ou pares ou numeros repetidos
  <li> filtro: se caso a soma dos numeros for maior que 250 e menor que 150 sera retirada
  <li> filtro: se a soma dos numeros da ultima sequencia da mega sena for igual a soma da sequencia gerada, ela sera excluida
  <li> filtro: se caso o intervalo da ultima sequencia da mega sena for igual e no mesmo lugar que da sequencia gerada, ela sera excluida
  <li> filtro: retira sequencias que sejam simetricas
  <li> filtro: pega todas as sequencias anteriores dá mega sena, se caso tiver mais que 3 numeros iguais, no mesmo lugar, é retirada
  <li> filtro: retira a sequencia que não tiver pelo menos um numero em cada quadrante
  <li> filtro: retira as sequencias que tiver os numeros na lista de intervalos simétricos a partir do intervalo da ultima sequencia da mega sena
</ol>
