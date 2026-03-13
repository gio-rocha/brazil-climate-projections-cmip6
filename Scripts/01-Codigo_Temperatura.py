# SCRIPT PARA MAPA DE MUDANÇA NA TEMPERATURA MÉDIA DO AR

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
import geopandas as gpd
import os
from matplotlib.colors import ListedColormap

#CORES------------------------------------------------------------------------------
#Escolhendo a fonte
fonte_gl={'family':'Arial','size': 16, 'color': 'black'}


cbar_kwargs={'orientation':'horizontal','fraction':0.045,'pad':0.01,'extend':'neither'}

escala_temp= np.arange(0, 5.5, 0.5)

tick_temp= np.arange(0, 5.5, 0.5)

colors_temp= ['#ffffff','#ffebb8','#facb55','#f2b317','#f7a975','#f27724','#fbbcbc','#f98f8f','#f54444','#f21515','#be4141','#960e0e']

#Adicionando as cores para posteriormente agregá-las ao mapa
cmap_temp= ListedColormap(colors_temp)

#Estabelecendo, respectivamente, a cor do topo e da base da barra
cmap_temp.set_over('#5a0808') #vermelho bordô

cmap_temp.set_under('#c1e5fb') #azul claro

label='ºC'

# caminhos
pathin = '/content/Dados/CMIP6/'
 # dados originais (por cenários) organizados em pastas para cada modelo

cenario_nomes=['SSP2','SSP5']

ssp2_lp= []
ssp5_lp= []

arqs_Ttop10=os.listdir(pathin)
    #organiza as 10 subspastas (1 por modelo) em uma "lista"

#Criando laço de repetição para passar pela pasta principal e entrar na pasta de cada modelo
for i in range(len(arqs_Ttop10)):

    path_model= '/content/Dados/CMIP6/' + arqs_Ttop10[i] + '/tas/'
     #O path_model abre a pasta de temperatura do modelo selecionado acima
     #neste caso, cada pasta (do modelo) contém 1 subpasta para temperatura e outra para precipitação, por isso o "/tas/"

    arqs_Tmod= os.listdir(path_model)


#Criando laço de repetição secundário pra acessar os dois arquivos (1 para cada cenário) contidos na pasta de temperatura
    for a in range(len(arqs_Tmod)):

        #Criando variável para receber o nome do arquivo
        arq= arqs_Tmod[a]

        #Abrindo o arquivo
        ds_temp= xr.open_dataset(path_model + arq)

        #Selecionando os dados de temperatura dentro do arq netcdf, selecionando as coordenadas para a AS, e selecionando o período de tempo (longo prazo)
        modelo= ds_temp['tas'].sel(lat=slice(-60,15),lon=slice(275,330),time=slice('2081','2100'))

        temp_convertida = modelo - 273.15
        # conversão de Kelvin para ºC

        #Tirando a média temporal
        media_fut = temp_convertida.mean(dim="time")

        #Condicionais para adicionar o resultado na lista adequada
        if cenario=='SSP2':

            ssp2_lp.append(media_fut)

        if cenario=='SSP5':

            ssp5_lp.append(media_fut)


futuro= [ssp2_lp, ssp5_lp]

#--------------------------------- MÉDIA DO HISTORICAL --------------------------------
arqs_hist = os.listdir('/content/Dados/Historical/')
#organiza as 10 subpastas (1 por modelo) em uma "lista"

hist_temp= [] #lista para receber a média temporal de cada modelo

for i in range(len(arqs_hist)):

    path_model_hist= '/content/Dados/Historical/' + arqs_hist[i] + '/tas/tas_historical_1995-2014.nc'
        #O path_model abre a pasta de temperatura dos dados historical selecionada acima

    ds_hist= xr.open_dataset(path_model_hist)

    temp_hist= ds_hist['tas'].sel(lat=slice(-60,15),lon=slice(275,330),time=slice('1995','2014'))

    temp_convert_hist= temp_hist - 273.15

    #Tirando a média temporal
    media_hist = temp_convert_hist.mean(dim="time")

    #adicionando na lista
    hist_temp.append(media_hist)

#------------------------------------- MÉDIA CLIMATOLÓGICA--------------------------------

#Fica fora do laço pois no clima presente os dados independem do cenário
clima_hist = (sum(hist_temp))/10 # tirando a média do conjunto para o presente

# LISTA PARA ARMAZENAR A MUDANÇA
clima_fut = [[],[]] # uma sublista para cada cenário

for c in range(0,2):

  media_fut = (sum(futuro[c]))/10  #tirando a média do conjunto para o futuro

  clima_fut[c].append(media_fut) #adicionado na lista de acordo com o cenário


mudanca_ssp2 = []
mudanca_ssp5 = []

for cen in range(0,2):

    #calculando a mudança de acordo com o cenário para o clima futuro
    dif_cen= clima_fut[cen][0] - clima_hist

    if cen==0: #condicionantes para adicionar na lista adequada
      mudanca_ssp2.append(dif_cen)

    if cen==1:
      mudanca_ssp5.append(dif_cen)


#FIGURA (composta de dois mapas) GERADA ABAIXO

  # Determinando tamanho e projeção dos dois mapas
fig,ax= plt.subplots(1, 2, figsize=(12,5.5),subplot_kw=dict(projection=ccrs.PlateCarree()))

#MAPA SSP2
ssp2_mapa = ax[0].contourf(mudanca_ssp2[0].lon, mudanca_ssp2[0].lat, mudanca_ssp2[0], cmap=cmap_temp, levels=escala_temp, extend='both', transform=ccrs.PlateCarree())

ax[0].set_extent([-75,-30,-35,6])  #recorte para dar destaque ao Brasil

ax[0].set_title("SSP2-4.5", fontweight= 'bold', fontsize= 14)
#título que aparece em cima do mapa à esquerda


#MAPA SSP5-------------------------------------------------------------

ssp5_mapa = ax[1].contourf(mudanca_ssp5[0].lon, mudanca_ssp5[0].lat, mudanca_ssp5[0], cmap=cmap_temp, levels=escala_temp, extend='both', transform=ccrs.PlateCarree())

ax[1].set_extent([-75,-30,-35,6])

ax[1].set_title("SSP5-8.5", fontweight= 'bold', fontsize= 14)
#título do mapa que aparece à direita


  #Adicionando o shape no mapa
brasil_shp = gpd.read_file('/content/Shapefiles/Regioes_Brasil.shp')

for eixo in ax:

  eixo.coastlines() #para exibir as linhas da costa da AS

  eixo.add_feature(cfeature.BORDERS) # para exibir as fronteiras da AS

    #Adicionando na camada superior a geometria com as regiões do Brasil
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


  fig.suptitle('Mudança da Temperatura Média (ºC) entre 2081-2100 \n (TOP10-CMIP6-AS)', fontweight= 'bold', fontsize= 14, y=0.95)

        # Construção da barra que vai na lateral do mapa
cbar = fig.colorbar(ssp2_mapa,ax=ax, orientation='vertical', fraction=0.03,pad=0.04,ticks=tick_temp)

cbar.ax.set_title(label, fontsize=16)

cbar.ax.tick_params(labelsize=14, width=1, length=5)

pathout= '/content/Figuras/'

plt.savefig(pathout + 'nome-da-figura.png', dpi=300, bbox_inches= 'tight')

plt.show()
