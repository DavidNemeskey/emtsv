#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys

import jnius_config

# DummyTagger (EXAMPLE) ################################################################################################

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'Dummy'))  # Needed to be able to use git submodule...
from DummyTagger.dummy import DummyTagger

# Setup the triplet: class, args (tuple), kwargs (dict)
dummy_tagger = (DummyTagger, ('Params goes here', {'Source field names'}, ['Target field names']), {})


# emToken ##############################################################################################################

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'emtokenpy'))  # Needed to be able to use git submodule...
from emtokenpy import EmTokenPy

em_token = (EmTokenPy, (), {'source_fields': set(), 'target_fields': ['string']})

# emMorph ##############################################################################################################

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'emmorphpy'))  # Needed to be able to use git submodule...
from emmorphpy import EmMorphPy

em_morph = (EmMorphPy, (), {'source_fields': {'string'}, 'target_fields': ['anas']})

# emTag ################################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'purepospy'))  # Needed to be able to use git submodule...
from purepospy import PurePOS
jnius_config.add_classpath(PurePOS.class_path)

em_tag = (PurePOS, (), {'source_fields': {'string', 'anas'},
                        'target_fields': ['lemma', 'hfstana']})

# emDepTool ############################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'deptoolpy'))  # Needed to be able to use git submodule...
from deptoolpy.deptoolpy import DepToolPy
jnius_config.add_classpath(DepToolPy.class_path)

em_deptool = (DepToolPy, ({'string', 'lemma', 'hfstana'}, ['pos', 'feature']), {})

# emMorph2Dep ##########################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emmorph2ud'))  # Needed to be able to use git submodule...
from emmorph2ud.converter import EmMorph2UD

em_morph2ud = (EmMorph2UD, ({'string', 'lemma', 'hfstana'}, ['pos', 'feature']), {})

# emChunk ##############################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'HunTag3'))
from huntag.tagger import Tagger as EmSeqTag
from huntag.tools import get_featureset_yaml, data_sizes

model_name = os.path.join(os.path.dirname(__file__), 'models', 'emChunk', 'maxNP-szeged-hfst')
cfg_file = 'HunTag3/configs/maxnp.szeged.hfst.yaml'
tag_field = 'NP-BIO'

options = {'model_filename': '{0}{1}'.format(model_name, '.model'),
           'featcounter_filename': '{0}{1}'.format(model_name, '.featureNumbers.gz'),
           'labelcounter_filename': '{0}{1}'.format(model_name, '.labelNumbers.gz'),
           'tag_field': tag_field,
           'data_sizes': data_sizes,
           'transmodel_filename': '{0}{1}'.format(model_name, '.transmodel'),
           'target_fields': ['NP_BIO'],
           'task': 'tag'
           }

features = get_featureset_yaml(cfg_file)

em_chunk = (EmSeqTag, (features, options), {})

# emDep ################################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emdeppy'))  # Needed to be able to use git submodule...
from emdeppy import EmDepPy
jnius_config.add_classpath(EmDepPy.class_path)

em_dep = (EmDepPy, (), {'source_fields': {'string', 'lemma', 'pos', 'feature'},
                        'target_fields': ['tokid', 'deptype', 'deptarget']})

# emDep ################################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emdeppy'))  # Needed to be able to use git submodule...
from emdeppy import EmDepPy
jnius_config.add_classpath(EmDepPy.class_path)

em_depud = (EmDepPy, (), {'source_fields': {'string', 'lemma', 'pos', 'feature'},
                          'target_fields': ['tokid', 'deptype', 'deptarget'],
                          'model_file': os.path.join(os.path.dirname(os.path.abspath(
                              sys.modules[EmDepPy.__module__].__file__)), 'szk.mate.ud.model')})

# emCons ###############################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emconspy'))  # Needed to be able to use git submodule...
from emconspy import EmConsPy
jnius_config.add_classpath(EmConsPy.class_path)
jnius_config.add_options(EmConsPy.vm_opts)
em_cons = (EmConsPy, (), {'source_fields': {'string', 'lemma', 'hfstana'},
                          'target_fields': ['tokid', 'cons'],
                          'model_file': os.path.join(os.path.dirname(os.path.abspath(
                              sys.modules[EmConsPy.__module__].__file__)), 'szk.const.model')})

########################################################################################################################

# Map module personalities to firendly names...
tools = {'tok': em_token, 'emToken': em_token,
         'morph': em_morph, 'emMorph': em_morph,
         'pos': em_tag, 'emTag': em_tag,
         'chunk': em_chunk, 'emChunk': em_chunk,  # TODO: Chunk and NER model + NER config
         # Default is UD
         'conv-morph': em_morph2ud, 'conv-hfst2ud': em_morph2ud, 'conv-hfst2conll': em_deptool, 'emDepTool': em_deptool,
         'dep': em_depud, 'emDep-ud': em_depud, 'emDep-conll': em_dep, 'emDep': em_dep,
         'cons': em_cons, 'emCons': em_cons,
         }

presets = {'analyze': ['tok', 'morph', 'pos', 'chunk', 'conv-morph', 'dep', 'cons'],  # Full pipeline
           'tok-morph': ['tok', 'morph'],
           'tok-pos': ['tok', 'morph', 'pos'],
           'tok-chunk': ['tok', 'morph', 'pos', 'chunk'],
           'tok-dep': ['tok', 'morph', 'pos', 'conv-morph', 'dep'],
           'tok-cons': ['tok', 'morph', 'pos', 'cons'],
           }

# cat input.txt | ./emtsv.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./emtsv.py tok-dep
