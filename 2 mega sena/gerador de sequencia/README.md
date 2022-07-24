<p align="center"><img src="https://user-images.githubusercontent.com/59841892/172259927-c8463fb8-64b4-4490-beca-bd8ac044a693.png"></p>
<h1 align="center"> gerador de sequencia </h1>
<br>
usado para gerar sequencias aleatória pro jogo da mega sena, os filtros se baseam em estatistica e probabilidade.
Uma sequencia aleatória é gerada e então é passado pelos filtros escolhidos, as sequencias permitidas serão mostrada ao usuario.
<br>
as sequencias não são retiradas da internet, pro programa poder ser executado mesmo offline
<br>
filtro 1: retira os numeros das 3 ultimas sequencias da mega sena
<br>
filtro 2: retira a sequencia se tiver mais que dois intervalos igual, se tiver mais que 4 impares ou pares ou numeros repetidos
<br>
filtro 3: se caso a soma dos numeros for maior que 250 e menor que 150 sera retirada
<br>
filtro 4: se a soma dos numeros da ultima sequencia da mega sena for igual a soma da sequencia gerada, ela sera excluida
<br>
filtro 5: se caso o intervalo da ultima sequencia da mega sena for igual e no mesmo lugar que da sequencia gerada, ela sera excluida
<br>
filtro 6: retira sequencias que sejam simetricas
<br>
filtro 7: pega todas as sequencias anteriores dá mega sena, se caso tiver mais que 3 numeros iguais, no mesmo lugar, é retirada
<br>
filtro 8: retira a sequencia que não tiver pelo menos um numero em cada quadrante
<br>
filtro 9: retira as sequencias que tiver os numeros na lista de intervalos simétricos a partir do intervalo da ultima sequencia da mega sena
