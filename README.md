# Breeding Bird Survey
Analyzing BBS data for North America

Data files are not uploaded to this repo given size restrictions. Please, fetch the content of `50-StopData` [here](https://tinyurl.com/ywtxx44u) if needed.

This script only uses 50 Stop Data. The main output is a dictionary with a time series for each species and route.

Local file tree:

``` text
> bbs$ tree 
.
├── 50-StopData
│   ├── Fifty10.csv
│   ├── Fifty1.csv
│   ├── Fifty2.csv
│   ├── Fifty3.csv
│   ├── Fifty4.csv
│   ├── Fifty5.csv
│   ├── Fifty6.csv
│   ├── fifty7.csv
│   ├── Fifty8.csv
│   └── Fifty9.csv
├── LICENSE
├── MigrantNonBreeder.zip
├── README.md
├── Routes.csv
├── SpeciesList.csv
├── ts_processing.ipynb
└── Weather.csv

```

## Plan de ruta

Hacer:
- Series temporales de un misma especie en distintos sitios. Puede ser para dos especies  una de amplia distribuciòn y una de distribuciòn restringida.
- Las series temporales son de los numeros totales y hay que seleccionar unos 5 sitios por especies, los que tengan pocos ceros.
- Lo otro es tomar un sitio y sacar las series temporales para todas las especies——
- Luego te explico lo de la riqueza…y te voy a mandar el link al paper en overleaf...