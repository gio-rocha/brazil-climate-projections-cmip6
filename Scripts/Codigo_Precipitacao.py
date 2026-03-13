#SCRIPT PARA PRECIPITAÇÃO

######### IMPORTANDO BIBLIOTECAS ###########
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
from cartopy.io.shapereader import Reader
import numpy as np
from xarray import *
import xarray as xr
import os
import geopandas as gpd
from matplotlib.colors import ListedColormap

#CORES------------------------------------------------------------------------------
#Escolhendo a fonte
fonte_gl={'family':'Arial','size': 16, 'color': 'black'}


cbar_kwargs={'orientation':'horizontal','fraction':0.045,'pad':0.01,'extend':'neither'}

escala_precip=np.arange(-50,60,10)

tick_precip=np.arange(-50,60,10)


colors_precip=['#62391a','#896448','#ad834c','#c0a26a','#d5c19b','#afc9c6','#add9d3','#5acfbe','#6aa49c','#458d83','#1a5d57']


#Adicionando as cores no mapa
cmap_precip=ListedColormap(colors_precip)


#Escolhendo as cores das extremidades da legenda
cmap_precip.set_over('#00271e')    #extremidade do topo: verde água em tom forte

cmap_precip.set_under('#431b01')   # extremidade da base: marrom

label ='%'  # símbolo que ficará acima da barra para representar a unidade considerada na análise

# caminhos
pathin = '/content/Dados/CMIP6/'

cenario_nomes=['SSP2','SSP5']

ssp2_lp= []
ssp5_lp= []

arqs_Ptop10=os.listdir(pathin) #transformando os nomes das 10 pastas em uma lista para organizar o acesso

#Criando laço de repetição para passar pela pasta principal e entrar na pasta de cada modelo
#Foi criada 1 pasta para cada modelo e uma subpasta para cada variável climática estudada (temp e precip)

for i in range(len(arqs_Ptop10)):

    path_model= '/content/drive/MyDrive/Dados_TCC/CMIP6/' + arqs_Ptop10[i] + '/pr/'
     #O path_model abre a pasta de precipitação do modelo selecionado acima

    arqs_Pmod= os.listdir(path_model)

#Criando laço de repetição secundário pra fazer busca pela variável 'pr' na pasta de cada modelo
    for a in range(len(arqs_Pmod)):

        #Criando variável para receber o nome do arquivo
        arq= arqs_Pmod[a]

        #Abrindo o arquivo desejado
        ds_pr= xr.open_dataset(path_model + arq)

        #Selecionando a variável climática, as coordenadas da AS, e o recorte temporal do clima futuro (longo prazo)
        modelo= ds_pr['pr'].sel(lat=slice(-60,15),lon=slice(275,330),time=slice('2081','2100'))

      #Conversão
        pr_convertida = modelo * 86400

        #Tirando a média temporal
        media_fut = pr_convertida.mean(dim="time")

  #Condicionais para adicionar a média temporal de cada modelo na lista certa de acordo com o cenário
        if cenario=='SSP2':

            ssp2_lp.append(media_fut)


        if cenario=='SSP5':

            ssp5_lp.append(media_fut)


futuro= [ssp2_lp, ssp5_lp]

#--------------------------------- MÉDIA BRUTA DO HISTORICAL --------------------------------
arqs_hist = os.listdir('/content/Dados/Historical/')
#lista que organiza os nomes das pastas (1 pasta por modelo)

hist_pr= []

for i in range(len(arqs_hist)):

    path_model_hist= '/content/Dados/Historical/' + arqs_hist[i] + '/pr/pr_historical_1995-2014.nc'
                        #O path_model abre a pasta de precipitação dos dados historical selecionada acima

  #abrindo o arquivo desejado
    ds_hist= xr.open_dataset(path_model_hist)

  #selecionando a variável climática, selecionando as coordenadas da AS, selecionando o recorte temporal desejado
    pr_hist= ds_hist['pr'].sel(lat=slice(-60,15),lon=slice(275,330),time=slice('1995','2014'))

    pr_convert_hist= pr_hist * 86400

    #Tirando a média temporal
    media_hist = pr_convert_hist.mean(dim="time")

  #adicionando na lista
    hist_pr.append(media_hist)


#------------------------------------- MÉDIA CLIMATOLÓGICA--------------------------------
clima_hist = (sum(hist_pr))/10
#calculando a média do conjunto para o clima presente

# LISTA PARA ARMAZENAR A MUDANÇA 
clima_fut = [[],[]] #1 sublista para cada cenário

for c in range(0,2):
  #calculando a média do conjunto para o clima futuro
  media_fut = (sum(futuro[c]))/10

  #adicionando na lista adequada
  clima_fut[c].append(media_fut)


mudanca_ssp2 = []
mudanca_ssp5 = []

for cen in range(0,2):
  #Calculando a mudança e convertendo para percentual
    dif_cen= ((clima_fut[cen][0] - clima_hist) / clima_hist) * 100

    if cen==0:
      mudanca_ssp2.append(dif_cen)

    if cen==1:
      mudanca_ssp5.append(dif_cen)


#FIGURA (com dois mapas - um para cada cenário) GERADA ABAIXO
  # Determinando tamanho e projeção dos dois mapas
fig,ax= plt.subplots(1, 2, figsize=(12,5.5),subplot_kw=dict(projection=ccrs.PlateCarree()))

#MAPA SSP2
ssp2_mapa = ax[0].contourf(mudanca_ssp2[0].lon, mudanca_ssp2[0].lat, mudanca_ssp2[0], cmap=cmap_precip, levels=escala_precip, extend='both', transform=ccrs.PlateCarree())

ax[0].set_extent([-75,-30,-35,6]) #coordenadas para focar o recorte no Brasil

ax[0].set_title("SSP2-4.5", fontweight= 'bold', fontsize= 14)
#título que vai aparecer acima do mapa à esquerda


#MAPA SSP5
ssp5_mapa = ax[1].contourf(mudanca_ssp5[0].lon, mudanca_ssp5[0].lat, mudanca_ssp5[0], cmap=cmap_precip, levels=escala_precip, extend='both', transform=ccrs.PlateCarree())

ax[1].set_extent([-75,-30,-35,6]) #coordenadas para focar o recorte no Brasil

ax[1].set_title("SSP5-8.5", fontweight= 'bold', fontsize= 14)
# título que vai aparecer acima do mapa à direita


#Abrindo o shape com as cinco regiões do Brasil
brasil_shp = gpd.read_file('/content/Shapefiles/Regioes_Brasil.shp')

for eixo in ax:

  eixo.coastlines() #adicionando as linhas da costa da AS

  eixo.add_feature(cfeature.BORDERS) #adicionando as linhas das fronteiras da AS

  #adicionando o recorte das cinco regiões do Brasil nos dois mapas
  eixo.add_geometries(
          brasil_shp.geometry,
          ccrs.PlateCarree(),
          edgecolor='black',
          facecolor='none',
          linewidth=1.5)

        #Colocando grade de coordenadas nas figuras
  fonte_gl_coord={'family':'serif', 'size':12,'color':'black'}
  gl=eixo.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,alpha=0)
  gl.top_labels=False ; gl.bottom_labels=True
  gl.left_labels=True ; gl.right_labels=False
  gl.xpadding= 4 ; gl.ypadding=4
  gl.xlabel_style= fonte_gl_coord ; gl.ylabel_style= fonte_gl_coord

  # Escolhendo fonte para título
  plt.rcParams['font.family'] = 'Serif'

  plt.rcParams['axes.unicode_minus'] = False  #para aceitar os números negativos também

  #exemplo de título
  fig.suptitle('Mudança na Precipitação Total (%) entre 2081-2100 \n (TOP10-CMIP6-AS)', fontweight= 'bold', fontsize= 14, y=0.95)

        # Construção da barra que vai na lateral do mapa
cbar = fig.colorbar(ssp2_mapa,ax=ax, orientation='vertical', fraction=0.03,pad=0.04,ticks=tick_precip)

cbar.ax.set_title(label, fontsize=16)

cbar.ax.tick_params(labelsize=14, width=1, length=5)

pathout= '/content/drive/MyDrive/Resultados_Colab/Figuras/'

plt.savefig(pathout + 'nome-da-figura.png', dpi=300, bbox_inches= 'tight')

plt.show()
