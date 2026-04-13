# Brazil-Climate-Projections-CMIP6

# Overview
  This repository contains Python scripts developed to analyze future climate projections over Brazil using CMIP6 models outputs.

# Objectives
 - Evaluate long-term projected temperature changes over Brazil based on CMIP6 ensemble means
 - Compare present and future climate scenarios
 - Generate spatial maps for SSP2-4.5 and SSP5-8.5 scenarios (2081-2100)

# Data Sources
 - *Original CMIP6 data* [Access the data](https://esgf-node.ipsl.upmc.fr/search/cmip6-ipsl/)
 - 10 CMIP6 models outputs: ACCESS-ESM1-5; CMCC-ESM2; CNRM-ESM2-1; EC-Earth3; INM-CM5-0; KACE-1-0-G; MIROC6; MPI-ESM1-2-HR; MRI-ESM2-0; TAIESM1
 - *Brazilian Major Regions (Grandes Regiões)*
   - Source: IBGE – Instituto Brasileiro de Geografia e Estatística  
   - Description: Official regional division of Brazil into five major regions (North, Northeast, Central-West, Southeast, and South)
   - 🔗 [Download Data](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2025/Brasil/BR_Regioes_2025.zip)


# Tools and Libraries
 - Python
 - Xarray
 - Numpy
 - Matplotlib
 - Cartopy
 - Geopandas

# Methodology
 - Mean temperature change (ºC)
 - Total precipitation change (%)
 - SSP2-4.5 and SSP5-8.5 scenarios
 - Ensemble mean using 10 models (TOP10-CMIP6-AS)
 - Historical period: 1995-2014
 - Future period: 2081-2100
   
# Outputs
 - Regional climate change analysis (temperature and precipitation)
   <img width="3099" height="1446" alt="Pr_Regioes-Br_LP" src="https://github.com/user-attachments/assets/a1ef051e-e11d-4a64-985b-7abe5ba001e2" />
<img width="3097" height="1446" alt="Tas_Regioes-Br_LP" src="https://github.com/user-attachments/assets/f7bf402c-e4b3-404b-8d3a-d2169be50e05" />

