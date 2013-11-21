{'application':{'type':'Application',
          'name':'Minimal',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':u'Circuitscape',
          'size':(972, 652),
          'backgroundColor':(230, 230, 230),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileLoadLast',
                   'label':u'Load settings from last run\tCtrl+L',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileLoadPrev',
                   'label':u'Load settings from file\tCtrl+O',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileSave',
                   'label':'Save settings\tCtrl+S',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileVerifyCode',
                   'label':'Verify code',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileRunBatch',
                   'label':'Run in batch mode',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileAbout',
                   'label':'About Circuitscape...',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuOptions',
             'label':u'Options',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuOptionsCalculationOptions',
                   'label':'CALCULATION OPTIONS:',
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsPrintTimings',
                   'label':'   Display completion times in terminal',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsLowMemory',
                   'label':'   Pairwise mode: run in low memory mode',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsUnitSrcs',
                   'label':'   Advanced mode: use unit currents (i=1) for all current sources  ',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsDirectGnds',
                   'label':'   Advanced mode: use direct connections to ground (R=0) for all ground points',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsRmvGnd',
                   'label':'   Advanced mode: remove ground whenever a source and ground conflict',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsRmvSrc',
                   'label':'   Advanced mode: remove source whenever a source and ground conflict',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsMappingOptions',
                   'label':'MAPPING OPTIONS:',
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsCompressGrids',
                   'label':'   Compress output grids',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsLogCurMap',
                   'label':'   Log-transform current maps',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsCumMap',
                   'label':'   Write cumulative current map only',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsBeta',
                   'label':'BETA OPTIONS (These are in development.  See user guide):',
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsMaxMap',
                   'label':'  Write maximum of current maps',
                   'checkable':1,
                  },                  
                  {'type':'MenuItem',
                   'name':'menuOptionsMask',
                   'label':'  Read mask file',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsVarSrc',
                   'label':'  One-to-all and All-to-one modes: read source strength file',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsIncludePairs',
                   'label':'  Read file with focal node pairs to include/exclude',
                   'checkable':1,
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'Choice', 
    'name':'scenarioChoice', 
    'position':(25, 87), 
    'size':(444, -1), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'items':['(Choose your modeling mode)', 'Pairwise: iterate across all pairs in focal node file', 'One-to-all: activate one focal node at a time with others grounded', 'All-to-one: ground one focal node at a time with others activated', 'Advanced: activate independent sources and grounds'], 
    'stringSelection':'(Choose your modeling mode)', 
    },

{'type':'Image', 
    'name':'Image1', 
    'position':(7, 0), 
    'backgroundColor':(230, 230, 230, 255), 
    'file':'cs_logo.jpg', 
    },

{'type':'StaticText', 
    'name':'CIRCUITSCAPE', 
    'position':(90, 12), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 24}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'CIRCUITSCAPE', 
    },

{'type':'StaticText', 
    'name':'scenarioText', 
    'position':(14, 65), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 13}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Source/ground modeling mode', 
    },

{'type':'StaticLine', 
    'name':'StaticLine1', 
    'position':(16, 124), 
    'size':(458, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine2', 
    'position':(492, 41), 
    'size':(-1, 370), 
    'layout':'vertical', 
    },

{'type':'StaticText', 
    'name':'inputHabitatData', 
    'position':(511, 11), 
    'font':{'style': 'bold', 'faceName': 'Lucida Grande', 'family': 'sansSerif', 'size': 13}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Input habitat data', 
    },

{'type':'StaticText', 
    'name':'rasterHabitatMapAndDataType', 
    'position':(522, 31), 
    'font':{'style': 'bold', 'faceName': 'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Raster habitat map and data type', 
    },

{'type':'StaticText', 
    'name':'pairwiseOptionsTitle', 
    'position':(14, 139), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 13}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Pairwise mode options', 
    },

{'type':'StaticText', 
    'name':'srcTargetFileText', 
    'position':(26, 160), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Focal node location file and data type', 
    },

{'type':'StaticLine', 
    'name':'StaticLine1111', 
    'position':(513, 168), 
    'size':(445, -1), 
    'layout':'horizontal', 
    },

{'type':'TextField', 
    'name':'srcTargetFile', 
    'position':(26, 181), 
    'size':(363, 21), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'text':'(Browse for a file with focal points or regions)', 
    },

{'type':'Button', 
    'name':'srcTargetBrowse', 
    'position':(396, 180), 
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 11}, 
    'label':'Browse', 
    },

{'type':'StaticText', 
    'name':'cellSchemeText', 
    'position':(508, 182), 
    'font':{'style': 'bold', 'faceName': 'Lucida Grande', 'family': 'sansSerif', 'size': 13}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Cell connection scheme and calculation', 
    },

{'type':'Choice', 
    'name':'focalNodeChoice', 
    'position':(26, 209), 
    'size':(444, -1), 
    'font':{'faceName': 'Tahoma', 'family': 'sansSerif', 'size': 11}, 
    'items':['(Choose one: nodes represent focal POINTS or focal REGIONS)', 'Focal POINTS: Each focal node contains one cell (FASTEST)', 'Focal REGIONS: Focal nodes may contain multiple cells'], 
    },

{'type':'StaticLine', 
    'name':'StaticLine11', 
    'position':(16, 243), 
    'size':(458, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticText', 
    'name':'advancedOptionsTitle', 
    'position':(14, 255), 
    'font':{'style': 'bold', 'faceName': 'Lucida Grande', 'family': 'sansSerif', 'size': 13}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Advanced mode options', 
    },

{'type':'StaticLine', 
    'name':'StaticLine111', 
    'position':(513, 263), 
    'size':(445, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticText', 
    'name':'srcFileText', 
    'position':(26, 276), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Current source file', 
    },

{'type':'TextField', 
    'name':'currentSrcFile', 
    'position':(26, 297), 
    'size':(363, 21), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'text':'(Browse for a current source file)', 
    },

{'type':'Button', 
    'name':'currentSrcBrowse', 
    'position':(396, 296), 
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 11}, 
    'label':'Browse', 
    },

{'type':'StaticText', 
    'name':'outputOptions', 
    'position':(509, 277), 
    'font':{'style': 'bold', 'faceName': 'Lucida Grande', 'family': 'sansSerif', 'size': 13}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Output options', 
    },

{'type':'StaticText', 
    'name':'outFileText', 
    'position':(522, 298), 
    'font':{'style': 'bold', 'faceName': 'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Base output file name', 
    },

{'type':'StaticText', 
    'name':'gndFileText', 
    'position':(26, 329), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Ground point file and data type', 
    },

{'type':'TextField', 
    'name':'gndFile', 
    'position':(26, 350), 
    'size':(363, 21), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'text':'(Browse for a ground point file)', 
    },

{'type':'Button', 
    'name':'gndBrowse', 
    'position':(396, 349), 
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 11}, 
    'label':'Browse', 
    },

{'type':'Choice', 
    'name':'gndResistanceChoice', 
    'position':(26, 379), 
    'size':(444, -1), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'items':['(Choose ground data type: RESISTANCE or CONDUCTANCE)', 'Ground values specify RESISTANCES', 'Ground values specify CONDUCTANCES '], 
    'stringSelection':'(Choose ground data type: RESISTANCE or CONDUCTANCE)', 
    },

{'type':'TextField', 
    'name':'habitatFile', 
    'position':(522, 52), 
    'size':(346, 21), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'text':'(Browse for a habitat map file)', 
    },

{'type':'Button', 
    'name':'habitatBrowse', 
    'position':(874, 51), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'label':'Browse', 
    },

{'type':'Choice', 
    'name':'habResistanceChoice', 
    'position':(522, 79), 
    'size':(427, -1), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'items':['(Choose habitat data type: RESISTANCE or CONDUCTANCE)', 'Habitat data specify per-cell RESISTANCES', 'Habitat data specify per-cell CONDUCTANCES'], 
    'stringSelection':'(Choose habitat data type: RESISTANCE or CONDUCTANCE)', 
    },

{'type':'CheckBox', 
    'name':'loadPolygonBox', 
    'position':(519, 112), 
    'size':(377, 21), 
    'font':{'style': 'bold', 'family': 'sansSerif', 'size': 11}, 
    'foregroundColor':(0, 0, 160, 255), 
    'label':'Optional: load a raster short-circuit region map', 
    },

{'type':'TextField', 
    'name':'polygonFile', 
    'position':(522, 136), 
    'size':(346, 21), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'text':'(Browse for a short-circuit region file)', 
    },

{'type':'Button', 
    'name':'polygonBrowse', 
    'position':(874, 135), 
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 11}, 
    'label':'Browse', 
    },

{'type':'Choice', 
    'name':'connSchemeChoice', 
    'position':(522, 205), 
    'size':(427, -1), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'items':['(Choose to connect cells to their FOUR or EIGHT neighbors)', 'Cell connection scheme: Connect FOUR neighbors', 'Cell connection scheme: Connect EIGHT neighbors'], 
    'stringSelection':'(Choose to connect cells to their FOUR or EIGHT neighbors)', 
    },

{'type':'Choice', 
    'name':'connCalcChoice', 
    'position':(522, 233), 
    'size':(427, -1), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'items':['(Choose how to calculate connections between neighbors)', 'Cell connection calculation: Average RESISTANCE', 'Cell connection calculation: Average CONDUCTANCE'], 
    'stringSelection':'(Choose how to calculate connections between neighbors)', 
    },

{'type':'StaticText', 
    'name':'outFileText1', 
    'position':(522, 353), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'What output maps do you want to produce?', 
    },

{'type':'TextField', 
    'name':'outFile', 
    'position':(522, 320), 
    'size':(346, 21), 
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 11}, 
    'text':'(Choose a base name for output files)', 
    },

{'type':'Button', 
    'name':'outBrowse', 
    'position':(874, 319), 
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 11}, 
    'label':'Browse', 
    },

{'type':'CheckBox', 
    'name':'curMapBox', 
    'position':(522, 378), 
    'size':(214, 13), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'label':'Current maps', 
    },

{'type':'CheckBox', 
    'name':'voltMapBox', 
    'position':(522, 404), 
    'size':(212, 20), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'label':'Voltage maps', 
    },

{'type':'Button', 
    'name':'calcButton', 
    'position':(818, 393), 
    'size':(127, -1), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 13}, 
    'label':'RUN', 
    },

{'type':'StaticLine', 
    'name':'StaticLine1', 
    'position':(14, 430), 
    'size':(935, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticText', 
    'name':'logWindowLabel', 
    'position':(14, 435), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 13}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Logs', 
    },

{'type':'StaticText', 
    'name':'logLevelText', 
    'position':(100, 438), 
    'font':{'style': 'bold', 'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':'Level', 
    },

{'type':'Choice', 
    'name':'logLevelChoice', 
    'position':(140, 432), 
    'size':(100, -1), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'items':['DEBUG', 'INFO', 'WARN', 'ERROR'], 
    'stringSelection':'DEBUG', 
    },

{'type':'CheckBox', 
    'name':'logRusageBox', 
    'position':(270, 435), 
    'size':(170, 20), 
    'font':{'faceName': u'Lucida Grande', 'family': 'sansSerif', 'size': 11}, 
    'label':'Log resource information', 
    },
                        
{'type':'Button', 
    'name':'clearLogsButton', 
    'position':(860, 430), 
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 11}, 
    'label':'Clear', 
    },

{'type':'TextArea', 
    'name':'logMessages', 
    'position':(20, 460), 
    'size':(935, 150), 
    'font':{'faceName': u'Lucida Grande', 'family': 'default', 'size': 11},
    'editable': 0 
    },

] # end components
} # end background
] # end backgrounds
} }
